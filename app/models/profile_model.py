from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Krishna User (Default)")
    title = models.CharField(max_length=100, default="This is the (Default)")
    desc_text = "Hey there is default text description"
    desc = models.CharField(max_length=200, null=True, default=desc_text)
    profile_img = models.ImageField(default="default.jpg", upload_to="profile/")

    phone = models.CharField(max_length=150, default="", null=True)
    address = models.TextField(null=False, default="")
    city = models.CharField(max_length=150, default="", null=True)
    state = models.CharField(max_length=150, default="", null=True)
    country = models.CharField(max_length=150, default="", null=True)
    pincode = models.CharField(max_length=150, default="", null=True)
    forget_password_token = models.CharField(max_length=100, default="token123", null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.user.username}'s profile"
