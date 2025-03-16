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
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.http import HttpRequest, HttpResponse
from app.models.user_model import UserModel
from app.models.profile_model import ProfileModel
from app.utils.user_utils import send_forget_password_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from app.utils.user_utils import TokenGenerator
from config import settings


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
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body.decode("utf-8"))
            else:
                data = request.POST
        except json.JSONDecodeError:
            return self._response(request, "Invalid JSON format", success=False)

        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if not all([new_password, confirm_password]):
            return self._response(request, "All fields are required.", success=False)

        if new_password != confirm_password:
            return self._response(request, "Passwords do not match.", success=False, token=token)

        try:
            profile_obj = ProfileModel.objects.get(forget_password_token=token)
            user = profile_obj.user
            user.set_password(new_password)
            user.save()
            return self._response(request, "Password changed successfully. Please login.", success=True)

        except ProfileModel.DoesNotExist:
            return self._response(request, "Invalid or expired token.", success=True)
    
    def _response(self, request, message, success=None, token=None):
        """
        Returns JSON response for API requests or renders HTML for web requests.

        Args:
            request (HttpRequest): The HTTP request instance.
            message (str): Response message.
            success (bool): Status of the operation.
            redirect_url (str): Optional URL for redirection.

        Returns:
            JsonResponse | HttpResponse: JSON response for API calls, HTML page for web requests.
        """
        if request.content_type == "application/json":
            response_data = {"success": success, "message": message}
            return JsonResponse(response_data, status=200 if success else 400)

        if success:
            messages.success(request, message)
            return redirect("/login")
        messages.error(request, message)
        return redirect(f"/change-password/{token}/")        

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
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body.decode("utf-8"))
            else:
                data = request.POST
        except json.JSONDecodeError:
            return self._response(request, "Invalid JSON format", success=False)

        email = data.get("email", "").strip()
        if not email:
            return self._response(request, "Please enter your email.", success=False)

        user = UserModel.objects.filter(email=email).first()
        
        if not user:
            return self._response(request, "No user found with this email.", success=False)

        if not user.is_active:
            self._send_confirmation_email(request, user)
            activation_msg = "Your account is not activated. Please check your email to activate your account."
            return self._response(request, activation_msg, success=False)

        token = str(uuid.uuid4())
        profile_obj, created = ProfileModel.objects.get_or_create(user=user)
        profile_obj.forget_password_token = token
        profile_obj.save()

        # Send the reset password email
        send_forget_password_mail(user.email, token)

        message = "An email has been sent with password reset instructions."
        return self._response(request, message, success=True)

    def _response(self, request, message, success=None):
        """
        Returns JSON response for API requests or renders HTML for web requests.

        Args:
            request (HttpRequest): The HTTP request instance.
            message (str): Response message.
            success (bool): Status of the operation.
            redirect_url (str): Optional URL for redirection.

        Returns:
            JsonResponse | HttpResponse: JSON response for API calls, HTML page for web requests.
        """
        if request.content_type == "application/json":
            response_data = {"success": success, "message": message}
            return JsonResponse(response_data, status=200 if success else 400)

        messages.error(request, message)
        return redirect("/forget-password/")
    
    def _send_confirmation_email(self, request: HttpRequest, user) -> None:
        """
        Sends an email confirmation link to the user.

        Args:
            request (HttpRequest): The HTTP request instance.
            user (UserModel): The newly created user.
        """
        current_site = get_current_site(request)
        email_subject = "Confirm your email address"
        message = render_to_string(
            "email-confirmation.html",
            {
                "name": user.first_name,
                "domain": current_site.domain,
                "uid": str(user.uid),
                "token": TokenGenerator().make_token(user),
            },
        )
        email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [user.email])
        email.fail_silently = True
        email.send()