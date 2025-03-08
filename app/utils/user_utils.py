"""
user_utils.py - Utility Functions for User Management

This module provides utility functions to simplify common user-related tasks.

Functions:
    get_user_profile(user): Retrieves the user's profile.
    create_user_profile(user, **kwargs): Creates a user profile.
    update_user_profile(user, **kwargs): Updates an existing user profile.
    is_user_active(user): Checks if a user is active.
    send_welcome_email(user): Sends a welcome email to a new user.

### Usage:
- Import functions from this module to perform common user operations.

"""

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render
from app.utils.common_utils import get_cart_count
from utils.common_utils import TokenGenerator


def get_user_from_uid(uidb64: str) -> User:
    """
    Decodes the base64 encoded UID and retrieves the associated user.

    Args:
        uidb64: The base64 encoded user ID.

    Returns:
        User instance or None if not found or invalid.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except (TypeError, OverflowError, User.DoesNotExist):
        return None


def activate_user(request:HttpRequest, user: User) -> None:
    """
    Activates the user account and logs them in.

    Args:
        user: The user to be activated.
    """
    user.is_active = True
    user.save()
    login(request, user)


def activate_account(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """
    Handles the activation of a user's account after registration.

    Decodes the UID, validates the activation token, and activates the user's account if valid. 
    Upon success, the user is logged in, and a success message is displayed. 
    If the activation fails, an error message is shown.

    Args:
        request: The HTTP request object.
        uidb64: The base64 encoded user ID.
        token: The token used for user activation.

    Returns:
        Rendered response with either a success or failure message.
    """
    user = get_user_from_uid(uidb64)

    if user is not None and TokenGenerator.check_token(user, token):
        activate_user(request, user)
        messages.success(request, "Registration complete. You are now logged in.")
        cart_count = get_cart_count(request.user)
        return render(request, "thankyouregister.html", {"cart_count": cart_count})
    
    messages.error(request, "Activation failed. Invalid or expired token.")
    return render(request, "activation-failed.html")
