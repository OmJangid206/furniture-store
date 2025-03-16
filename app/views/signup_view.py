"""
views/auth_views.py

This module defines the `SignUpView` class, responsible for handling user registration.

It provides functionalities to:
- Register new users.
- Validate email uniqueness and password confirmation.
- Send welcome and email confirmation messages.

Classes:
    - SignUpView: Handles user registration and email verification.
"""

import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse 
from django.views import View
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from app.models.profile_model import ProfileModel
from app.models.user_model import UserModel
from django.template.loader import render_to_string
from config import settings
from app.utils.user_utils import TokenGenerator


class SignUpView(View):
    """
    Handles user registration, including email verification and welcome messages.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Renders the signup page.

        Args:
            request (HttpRequest): The HTTP request instance.
        Returns:
            HttpResponse: Rendered signup page.
        """
        return render(request, "signup.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Processes user signup form submission, supporting both JSON and form data.

        Args:
            request (HttpRequest): The HTTP request instance.
        Returns:
            HttpResponse: JSON response for API calls or rendered signup page for web requests.
        """
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body.decode("utf-8"))
            else:
                data = request.POST
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format"}, status=400)

        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        confirm_password = data.get("confirmPassword", "")

        if not all([first_name, last_name, email, password, confirm_password]):
            return self._response(request, "All fields are required.", success=False)

        # Check if user exists and handle accordingly
        existing_user = self._handle_existing_user(request, email)
        if existing_user:
            return existing_user

        # Continue with registration since no existing user was found
        if password != confirm_password:
            return self._response(request, "Passwords do not match.", success=False)
        
        user = self._create_user(email, first_name, last_name, password)
        self._send_welcome_email(user)
        self._send_confirmation_email(request, user)

        return self._response(request, "Account created. Check your email for activation.", success=True)

    def _response(self, request, message, success=True):
        """
        Returns JSON response for API requests or renders HTML for web requests.

        Args:
            request (HttpRequest): The HTTP request instance.
            message (str): Response message.
            success (bool): Status of the operation.

        Returns:
            JsonResponse | HttpResponse: JSON response for API calls, HTML page for web requests.
        """
        if request.content_type == "application/json":
            return JsonResponse({"success": success, "message": message}, status=200 if success else 400)

        messages.success(request, message) if success else messages.error(request, message)
        return render(request, "signup.html")

    def _create_user(self, email: str, first_name: str, last_name: str, password: str) -> UserModel:
        """
        Creates a new user account.

        Args:
            email (str): User's email.
            first_name (str): User's first name.
            last_name (str): User's last name.
            password (str): User's password.
        Returns:
            UserModel: Created user instance.
        """
        user = UserModel.objects.create_user(email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()

        # Create ProfileModel instance for the new user
        ProfileModel.objects.create(user=user, name=f"{first_name} {last_name}")
        return user
 
    def _send_welcome_email(self, user: UserModel) -> None:
        """
        Sends a welcome email to the user.

        Args:
            user (UserModel): The newly created user.
        """
        subject = "Welcome to Shanti Furniture E-shop"
        message = f"Hello {user.first_name},\n\nWelcome to Shanti Furniture E-shop!\nThank you for signing up. Please check your email to activate your account."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)

    def _send_confirmation_email(self, request: HttpRequest, user: UserModel) -> None:
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

    def _handle_existing_user(self, request: HttpRequest, email: str) -> HttpResponse | None:
        """
        Checks if the user already exists and handles activation status.

        Args:
            request (HttpRequest): The HTTP request instance.
            email (str): Email to check.

        Returns:
            HttpResponse | None: Response if user exists, otherwise None.
        """
        existing_user = UserModel.objects.filter(email=email).first()
        if existing_user:
            if not existing_user.is_active:
                self._send_confirmation_email(request, existing_user)
                return self._response(
                    request, "Your account is not activated. Please check your email to activate your account.", success=True
                )
            return self._response(request, "Email already exists.", success=False)
        
        return None # User does not exist, continue with registration
