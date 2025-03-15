import datetime
from django.db.models import Sum, F, IntegerField, ExpressionWrapper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, View, FormView
from .models import Product, Coupons, Category, Order, OrderItems
from .cart import Cart
from django.contrib import messages
from .forms import ProductForm, UserOrderInfoForm, CouponForm
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class ProductsListView(ListView):
    queryset = Product.objects.all()
    template_name = "onlineshop/products.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    # Checks if user asked for a category OR search keyword
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug', None)
        search_keyword = self.request.GET.get("search")
        sort_keyword = self.request.GET.get("sort_by")
        sort_possibilities = ["created", "-created", "-price", "price"]

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = Product.objects.filter(category=category)

        if search_keyword:
            queryset = queryset.filter(title__contains=search_keyword)

        if sort_keyword and sort_keyword in sort_possibilities:
            queryset = queryset.order_by(sort_keyword)

        return queryset


class ProductDetailsView(DetailView):
    queryset = Product.objects.all()
    template_name = "onlineshop/product_details.html"
    context_object_name = "product"

    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        category_slug = self.kwargs.get('category_slug', None)
        product_slug = self.kwargs.get('product_slug', None)
        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(Product, slug=product_slug, category=category)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.get_object().id
        cart_data = self.cart.get_data()
        context["cart_count"] = next(
            (item['quantity'] for item in cart_data['items'] if item['product']['id'] == product_id), 0)
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        cart = Cart(request)
        if 'add' in request.POST:
            cart.add(product=product, quantity=1)
            messages.success(request, "Product added successfully to your cart.")
        elif 'remove' in request.POST:
            cart.delete(product.id)
            messages.error(request, "Product deleted from your cart.")
        return redirect(product.get_absolute_url())


class ProductDeleteView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk).delete()
        messages.success(request, "Product has been deleted successfully.")
        return redirect("shop:product_list")


class CreateProductView(FormView):
    form_class = ProductForm
    template_name = 'onlineshop/product_form.html'
    success_url = reverse_lazy('shop:product_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdateProductView(View):
    form_class = ProductForm
    template_class = "onlineshop/product_form.html"

    def setup(self, request, *args, **kwargs):
        self.instance = get_object_or_404(Product, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, pk):
        form = self.form_class(instance=self.instance)
        return render(request, self.template_class, {"form": form, "product": self.instance})

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES, instance=self.instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Product has been updated successfully!!")
            return redirect('shop:product_list')
        return render(request, self.template_class, {"form": form, "product": self.instance})


class CartManagementView(TemplateView):
    template_name = "onlineshop/cart.html"

    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)

        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if 'clear/' in request.path:
            self.cart.clear()
            return redirect('shop:cart')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = self.cart
        print(self.cart.get_data())
        return context

    @method_decorator(login_required)
    def post(self, request):
        Order.objects.filter(user=request.user, paid=False).delete()
        order = Order.objects.create(user=request.user)
        cart_data = self.cart.get_data()
        if cart_data['items']:
            for item in cart_data['items']:
                product = item['product']
                OrderItems.objects.create(order=order, product=item['instance'], price=product['price'],
                                          quantity=item['quantity'])
            self.cart.clear()
            messages.success(request, "Your order has been added successfully!")
            return redirect('shop:order')
        messages.error(request, "To submit an order, you have to fill your cart first!")
        return redirect('shop:cart')


class CartItemDeleteView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.delete(product_id)
        return redirect('shop:cart')


class ClientOrderManagementView(LoginRequiredMixin, ListView):
    template_name = 'onlineshop/orders.html'
    model = Order
    context_object_name = "orders"

    def setup(self, request, *args, **kwargs):
        self.coupon_form = CouponForm
        self.response = redirect('shop:order')
        self.info_form = UserOrderInfoForm()
        self.order = Order.objects.filter(user=request.user, paid=False).first()
        if self.order:
            user_address = request.COOKIES.get('user_address', None)
            if self.order.client_info:
                first_name, *last_name = self.order.client_info.split(" ", 1)
                last_name = last_name[0] if last_name else ""
            else:
                first_name, last_name = request.user.first_name, request.user.last_name

            if self.order.address:
                user_address = self.order.address

            self.info_form = UserOrderInfoForm(initial={
                'name': first_name, 'last_name': last_name, 'address': user_address
            })

        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return Order.objects.select_related("user").filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_queryset().filter(paid=False).exists():
            context['current_order'] = self.get_queryset().get(paid=False)
        context['coupon_form'] = self.coupon_form
        context['info_form'] = self.info_form
        return context

    def post(self, request):
        if 'coupon_form' in request.POST:
            form = CouponForm(request.POST)
            if not form.is_valid():
                messages.error(request, "Something went wrong. try again later!")
                return self.response
            now = datetime.datetime.now()
            coupon = Coupons.objects.filter(code=form.cleaned_data['code'], valid_from__lte=now, valid_until__gte=now, is_active=True)
            if coupon:
                self.order.coupon = coupon[0].discount
                self.order.save()
                messages.success(request, "Coupon has been added to your order successfully!!")
                return self.response
            messages.error(request, "Coupon is invalid or expired.")
            return self.response

        elif 'info_form' in request.POST:
            form = UserOrderInfoForm(request.POST)
            if not form.is_valid():
                messages.error(request, "Something went wrong. try again later!")
                return self.response

            self.order.address = form.cleaned_data['address']
            self.order.client_info = f"{form.cleaned_data['name']} {form.cleaned_data['last_name']}"
            self.order.save()
            self.response.set_cookie('user_address', form.cleaned_data['address'], max_age=60 * 60 * 24 * 30)  # 30 days
            messages.success(request, "Your shipping info has been successfully updated!")
            return self.response

        elif 'checkout' in request.POST:
            if not self.order.address or not self.order.client_info:
                messages.error(request, "Please confirm your shipping info first.")
                return self.response
            messages.warning(request, "This website is a demo. So we will pretend you paid ^-^")
            self.order.paid = True
            self.order.save()
            with transaction.atomic():
                paid_orders = list(Order.objects.filter(user=self.order.user, paid=True).order_by('created')[:5])
                if len(paid_orders) >= 10:
                    paid_orders[0].delete()
            return self.response

        elif 'delete' in request.POST:
            self.order.delete()
            messages.success(request, "Your order has been deleted successfully!")
            return self.response

        return self.response




class AdminOrderManagementView(ListView):
    queryset = Order.objects.all()
    template_name = 'onlineshop/all_orders.html'
    context_object_name = 'orders'

    def setup(self, request, *args, **kwargs):
        if not request.user or not request.user.is_staff:
            return redirect('shop:product_list')
        return super().setup(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.GET.get("search")
        sort_keyword = self.request.GET.get("sort_by")
        sort_possibilities = ["created", "-created"]

        if search_keyword:
            queryset = queryset.filter(client_info__contains=search_keyword)

        if sort_keyword and sort_keyword in sort_possibilities:
            queryset = queryset.order_by(sort_keyword)

        if sort_keyword == 'total':
            queryset = queryset.annotate(
                total_price=ExpressionWrapper(
                    Sum(F("items__price") * F("items__quantity")),
                    output_field=IntegerField()
                )
            ).order_by("-total_price")

        return queryset


class AdminOrderUpdateView(View):
    def setup(self, request, *args, **kwargs):
        if not request.user or not request.user.is_staff:
            return redirect('shop:product_list')
        self.order = get_object_or_404(Order, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.order.status = request.POST['status']
        messages.success(request, "Order has been successfully updated.")
        self.order.save()
        return redirect('shop:order_all')

