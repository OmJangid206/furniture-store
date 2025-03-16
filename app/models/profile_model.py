"""
This module defines the `ProfileModel`, which extends the default Django `User` model 
to store additional user profile details.

Features:
- Associates a profile with each user account.
- Stores personal details such as name, title, and description.
- Includes contact information like phone, address, city, state, country, and pincode.
- Supports profile image storage using Cloudinary.
- Provides a password recovery token for account recovery.
- Tracks profile creation timestamps.

Classes:
- ProfileModel: A model that stores additional user details beyond the standard Django `User` model.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField


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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100, default="Unknown (default)")
    title = models.CharField(max_length=100, default="Untitled (default)")
    
    # Default description text
    description_text = "Hey this is default text description"
    description = models.CharField(max_length=200, null=True, default=description_text)
    
    # profile_img = models.ImageField(default="default.jpg", upload_to="profile/")
    # Upload profile images to Cloudinary instead of 'media/profile/'
    profile_img = CloudinaryField('profile', default="profile/default.jpg")
    phone = models.CharField(max_length=150, default='', null=True, blank=True)
    address = models.TextField(default='',null=True, blank=True)
    city = models.CharField(max_length=150,default='', null=True, blank=True)
    state = models.CharField(max_length=150, default='', null=True, blank=True)
    country = models.CharField(max_length=150, default='', null=True,  blank=True)
    pincode = models.CharField(max_length=150, default='', null=True, blank=True)
    
    # For password recovery
    forget_password_token = models.CharField(max_length=100, default='', null=True, blank=True)
    
    # Timestamp for when the profile was created
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = "profile"
        verbose_name_plural = "Profiles" 
        
    def __str__(self):
        """
        Returns a string representation of the profile.

        This method outputs the profile as a string in the format:
        "{username}'s profile", where {username} is the associated user's username.

        Returns:
            str: A string representation of the profile.
        """
        return f"{self.user.username}'s profile"
