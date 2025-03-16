"""
forms/user_form.py

User Registration and Profile Management Forms

This module defines Django forms for user registration and profile management.

Forms:
- `CreateUserForm`: Extends `UserCreationForm` to facilitate user sign-up.
- `ProfileForm`: Allows users to manage their profile details.

Usage:
    - Use `CreateUserForm` for user registration in authentication views.
    - Use `ProfileForm` to update profile details, including profile image.

"""

from django.contrib.auth.forms import UserCreationForm
from app.models.user_model import UserModel
from django.forms import ModelForm
from django.forms.widgets import FileInput
from app.models.profile_model import ProfileModel


class CreateUserForm(UserCreationForm):
    """
    Form for user registration.

    Inherits:
        UserCreationForm: Django's built-in user creation form.

    Meta:
        model (User): The Django built-in user model.
        fields (list): Fields required for user registration.
    """

    class Meta:
        model = UserModel
        fields = ["email", "password1", "password2"]


class ProfileForm(ModelForm):
    """
    Form for updating user profile.

    - Includes all fields from `ProfileModel`, except for `user`.
    - Uses a custom file input widget for profile image upload.

    Meta:
        model (ProfileModel): The profile model associated with the user.
        fields (str): Includes all fields except `user`.
        widgets (dict): Customizes the file input widget.
    """

    class Meta:
        model = ProfileModel
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "profile_img": FileInput(),
        }
