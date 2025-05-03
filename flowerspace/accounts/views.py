from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, LoginForm, OTPForm, ProfileEditForm
from django.contrib.auth.models import User
from django.views.generic import FormView, ListView
from django.views import View
from django.contrib.auth.views import LogoutView
from utils import send_otp, verify_otp
from .models import Profile, Relations
from django.contrib import messages
from home.models import Posts, BookMarks



class UserProfile(View):
    template_class = "accounts/profile.html"

    def setup(self, request, *args, **kwargs):
        queryset = Relations.objects.all()
        self.user = User.objects.get(username=kwargs['username'])
        self.user_posts = self.user.posts.prefetch_related('hashtags').all()
        self.is_following = False
        self.is_blocking = False
        if request.user.is_authenticated:
            relation = queryset.filter(from_user=request.user, to_user=self.user).first()
            if relation and not relation.is_blocking:
                self.is_following = True
            elif relation and relation.is_blocking:
                self.is_blocking = True
        self.followers_count = self.user.followings.filter(is_blocking=False).count()
        self.followings_count = self.user.followers.filter(is_blocking=False).count()
        return super().setup(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        context = {"user":self.user, "is_following":self.is_following, "is_blocking": self.is_blocking,
        "followers":self.followers_count, "followings": self.followings_count, "posts":self.user_posts}
        return render(request, self.template_class, context)



class UserProfileEdit(View):
    form_class = ProfileEditForm
    template_class = "accounts/profile_edit.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You are not authenticated.")
            return redirect("home:homepage")
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = self.form_class(instance=profile,
                               initial={"first_name":request.user.first_name, "last_name": request.user.last_name})
        return render(request, self.template_class, {"form":form, "profile":profile})

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        form = self.form_class(request.POST, request.FILES, instance=profile,
                               initial={"first_name":request.user.first_name})

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully! 🌸")
            return redirect('accounts:profile', request.user.username)




class UserRegister(FormView):
    template_name = "accounts/authentication.html"
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "You are already authenticated.")
            return redirect("home:homepage")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        del form.cleaned_data['password2']
        self.request.session['registration_data'] = form.cleaned_data
        send_otp(self.request, self.request.session['registration_data']['email'])
        messages.success(self.request, "Code has been sent. check your email!")
        return redirect('accounts:otp_check')

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = "register"
        return context



class UserLogin(FormView):
    template_name = "accounts/authentication.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "You are already authenticated.")
            return redirect("home:homepage")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(self.request, username=cd['email'], password=cd['password'])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Successfully logged in. welcome back {user.username}!")

            if self.request.GET.get("next"):
                return redirect(self.request.GET.get("next"))

            return redirect('home:homepage')
        else:
            messages.error(self.request, "Login info is invalid!")
            return redirect('accounts:login')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = "login"
        return context



class UserOtpConfirm(FormView):
    template_name = "accounts/authentication.html"
    form_class = OTPForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated or not request.session['registration_data']:
            messages.error(request, "You are already authenticated or dont have access to this endpoint.")
            return redirect("home:homepage")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if verify_otp(self.request.session['otp_code'], form.cleaned_data['otp_code']):
            user = self.request.session['registration_data']
            User.objects.create_user(username=user['username'], password=user['password1'], email=user['email'])
            user_check = authenticate(self.request, username=user['email'], password=user['password1'])
            login(self.request, user_check)
            del self.request.session['registration_data']
            messages.success(self.request, f"Successfully registered. welcome {user['username']}!")
        return redirect("home:homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = "otp"
        return context



class UserLogout(View):
    def get(self, request):
        logout(request)
        messages.warning(request, "You are no longer authenticated...you have limited access now!")
        return redirect("home:homepage")




class UserRelation(View):

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You cannot follow someone unless you are authenticated.")
            return redirect("accounts:profile", kwargs['username'])
        if request.user == self.user:
            messages.error(request, "You cannot follow yourself...silly.")
            return redirect("accounts:profile", kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, username):
        action = request.GET.get('action')

        if action == "follow":
            Relations.objects.filter(
                from_user=request.user,
                to_user=self.user,
                is_blocking=True
            ).delete()

            relation, created = Relations.objects.get_or_create(
                from_user=request.user,
                to_user=self.user,
                defaults={"is_blocking": False},
            )

            if not created:
                relation.delete()
                messages.success(request, "You unfollowed this user.")
            else:
                messages.success(request, "You followed this user!!")

        elif action == "block":
            Relations.objects.filter(
                from_user=request.user,
                to_user=self.user,
                is_blocking=False
            ).delete()

            relation, created = Relations.objects.get_or_create(
                from_user=request.user,
                to_user=self.user,
                defaults={"is_blocking": True},
            )

            if not created and relation.is_blocking:
                relation.delete()
                messages.warning(request, "You unblocked this user.")
            else:
                relation.is_blocking = True
                relation.save()
                messages.warning(request, "You blocked this user. Check rules for more info.")

        return redirect("accounts:profile", username)



class BookmarksView(LoginRequiredMixin, ListView):
    template_name = "accounts/bookmarks.html"
    context_object_name = "bookmarks"
    model = Posts

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.request.user.u_bookmark.all()
        return queryset
