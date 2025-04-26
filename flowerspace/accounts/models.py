from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from onlineshop.models import  Product


class Profile(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="pfp/", default="pfp/default.png")
    desc = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def get_absolute_url(self):
         return reverse("accounts:profile", args=[self.user.username])


class Relations(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    is_blocking = models.BooleanField(default=False)

    def __str__(self):
        if not self.is_blocking:
            return f"{self.from_user} is following {self.to_user}"
        return f"{self.from_user} is blocking {self.to_user}"

