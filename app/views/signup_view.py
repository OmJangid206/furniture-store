"""
views/auth_views.py

This module defines the `SignUpView` class responsible for handling user registration.

It provides functionalities to:
- Register new users.
- Validate email uniqueness and password confirmation.
- Send welcome and email confirmation messages.

Classes:
    - SignUpView: Handles user registration and email verification.
"""

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse 
from django.views import View
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
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
        Processes user signup form submission.

        Args:
            request (HttpRequest): The HTTP request instance.
        Returns:
            HttpResponse: Renders the signup page with messages.
        """
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "signup.html")

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")
        
        user = self._create_user(email, fname, lname, pass1)
        self._send_welcome_email(user)
        self._send_confirmation_email(request, user)

        messages.success(request, "Account created. Check your email for activation.")
        return render(request, "signup.html")

    def _create_user(self, email: str, first_name: str, last_name: str, password: str) -> User:
        """
        Creates a new user account.

        Args:
            email (str): User's email.
            first_name (str): User's first name.
            last_name (str): User's last name.
            password (str): User's password.
        Returns:
            User: Created user instance.
        """
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()
        return user

    def _send_welcome_email(self, user: User) -> None:
        """
        Sends a welcome email to the user.

        Args:
            user (User): The newly created user.
        """
        subject = "Welcome to Shanti Furniture E-shop"
        message = f"Hello {user.first_name},\n\nWelcome to Shanti Furniture E-shop!\nThank you for signing up. Please check your email to activate your account."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)

    def _send_confirmation_email(self, request: HttpRequest, user: User) -> None:
        """
        Sends an email confirmation link to the user.

        Args:
            request (HttpRequest): The HTTP request instance.
            user (User): The newly created user.
        """
        current_site = get_current_site(request)
        email_subject = "Confirm your email address"
        message = render_to_string(
            "email-confirmation.html",
            {
                "name": user.first_name,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": TokenGenerator().make_token(user),
            },
        )
        email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [user.email])
        email.fail_silently = True
        email.send()
