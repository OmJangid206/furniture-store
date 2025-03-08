"""
model/profile_model.py

This module contains the `ProfileModel` class that extends the default Django `User` model 
to store additional information related to a user's profile.

The `ProfileModel` class allows you to store extra details such as the user's name, title, 
description, contact information, profile image, and password recovery token. 

It ensures that each user has a unique profile associated with their account, which can be accessed 
and updated for a more personalized user experience.

Classes:
    ProfileModel (models.Model): A model for storing user profile details such as name, title, description, 
                                 profile image, and contact information.
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ProfileModel(models.Model):
    """
    Profile model that extends the default User model to store additional user details.

    This model stores additional information for a user, including personal details, contact information, 
    and a profile image. Each user can have one associated profile.

    Attributes:
        user (OneToOneField): The user associated with this profile.
        name (CharField): The name of the user in the profile.
        title (CharField): The title for the user in the profile.
        desc (CharField): A short description of the user.
        profile_img (ImageField): The user's profile image.
        phone (CharField): The user's phone number.
        address (TextField): The user's address.
        city (CharField): The user's city.
        state (CharField): The user's state.
        country (CharField): The user's country.
        pincode (CharField): The user's pincode.
        forget_password_token (CharField): Token used for password recovery.
        created_at (DateTimeField): The timestamp when the profile was created.

    Methods:
        __str__(): Returns a string representation of the profile in the format: "{username}'s profile".
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Krishna User (Default)")
    title = models.CharField(max_length=100, default="This is the (Default)")
    
    # Default description text
    desc_text = "Hey there is default text description"
    desc = models.CharField(max_length=200, null=True, default=desc_text)
    
    profile_img = models.ImageField(default="default.jpg", upload_to="profile/")

    phone = models.CharField(max_length=150, default="", null=True)
    address = models.TextField(null=False, default="")
    city = models.CharField(max_length=150, default="", null=True)
    state = models.CharField(max_length=150, default="", null=True)
    country = models.CharField(max_length=150, default="", null=True)
    pincode = models.CharField(max_length=150, default="", null=True)
    
    # For password recovery
    forget_password_token = models.CharField(max_length=100, default="token123", null=True)
    
    # Timestamp for when the profile was created
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        """
        Returns a string representation of the profile.

        This method outputs the profile as a string in the format:
        "{username}'s profile", where {username} is the associated user's username.

        Returns:
            str: A string representation of the profile.
        """
        return f"{self.user.username}'s profile"
