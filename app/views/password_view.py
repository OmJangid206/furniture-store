"""
view/password_view.py

This module contains views for handling password-related functionality, 
including password change and password recovery. These views are based on 
class-based views (CBVs) for better organization and reusability.

Views:
    ChangePasswordView: Handles the password change process.
    ForgetPasswordView: Handles the request to reset the password.
"""

import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpRequest, HttpResponse
from app.models.profile_model import ProfileModel
from app.utils.user_utils import send_forget_password_mail


class ChangePasswordView(View):
    """
    A class-based view that handles the password change process for the user.

    This view allows users to change their password using a token provided 
    (usually after a password reset request). If the passwords match, the 
    password is updated and the user is redirected to the login page.

    Methods:
        get: Displays the password change form.
        post: Handles the password change logic, verifying that the passwords match.
    """

    def get(self, request: HttpRequest, token: str) -> HttpResponse:
        """
        Displays the password change form.

        Args:
            request: The HTTP request object.
            token: The token used to identify the user for password change.

        Returns:
            Rendered change password page.
        """
        return render(request, "change-password.html", {"token": token})

    def post(self, request: HttpRequest, token: str) -> HttpResponse:
        """
        Handles the password change process.

        Verifies that the new password and confirm password match. If they do,
        it updates the user's password and redirects them to the login page.

        Args:
            request: The HTTP request object containing the new and confirm passwords.
            token: The token used to identify the user for password change.

        Returns:
            Redirect to the login page upon success or back to the change password form if error.
        """
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(f"/change-password/{token}/")

        try:
            profile_obj = ProfileModel.objects.get(forget_password_token=token)
            user = profile_obj.user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully. Please login.")
            return redirect("/login")
        except ProfileModel.DoesNotExist:
            messages.error(request, "Invalid token.")
            return redirect("/login")


class ForgetPasswordView(View):
    """
    A class-based view that handles the request for password reset.

    This view allows users to request a password reset. If a valid email is provided,
    a unique token is generated and associated with the user, which can be used to
    reset the password.

    Methods:
        get: Displays the password reset request form.
        post: Handles the password reset request logic.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Displays the password reset request form.

        Args:
            request: The HTTP request object.

        Returns:
            Rendered forget password page.
        """
        return render(request, "forget-password.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handles the password reset request.

        This method generates a token for the user, stores it in the profile model, 
        and sends an email with the token (email sending logic is commented out).

        Args:
            request: The HTTP request object containing the email input.

        Returns:
            Redirects the user to the forget password page with success or error message.
        """
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No user found with this email.")
            return redirect("/forget-password/")

        token = str(uuid.uuid4())
        profile_obj, created = ProfileModel.objects.get_or_create(user=user)
        profile_obj.forget_password_token = token
        profile_obj.save()

        # Call the email function
        send_forget_password_mail(user.email, token)

        messages.success(request, "An email is sent")
        return redirect("/forget-password/")
