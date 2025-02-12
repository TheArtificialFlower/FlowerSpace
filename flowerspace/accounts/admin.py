from django.contrib import admin
from .models import Profile, Relations
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        Profile.objects.get_or_create(user=obj)

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
admin.site.register(Relations)
