"""
views/auth_views.py

This module defines the `LoginView` class responsible for user authentication.

Features:
- Renders login page for unauthenticated users.
- Authenticates users and redirects based on `return_url`.
- Displays error messages for failed login attempts.

Classes:
    - LoginView: Handles user login.
"""
import json
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.core.mail import EmailMessage
from app.utils.user_utils import TokenGenerator
from app.middlewares.auth_middlewares import unauthentcated_user
from config import settings


@method_decorator(unauthentcated_user, name="dispatch")
class LoginView(View):
    """
    Handles user login and authentication.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Renders the login page and stores `return_url` for redirection after login.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            HttpResponse: Rendered login page.
        """
        request.session["return_url"] = request.GET.get("return_url")
        return render(request, "login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Processes user login form submission.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            HttpResponse: Redirects to `return_url` (if exists) or login page on failure.
        """
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body.decode("utf-8"))
            else:
                data = request.POST
        except json.JSONDecodeError:
            return self._response(request, "Invalid JSON format", success=False)

        email = data.get("email", "").strip()
        password = data.get("password", "")

        if not all([email, password]):
            return self._response(request, "All fields are required.", success=False)

        user = authenticate(request, email=email, password=password)

        if not user:
            return self._response(request, "Invalid email or password", success=False)

        if not user.is_active:
            self._send_confirmation_email(request, user)
            activation_msg = "Your account is not activated. Please check your email to activate your account."
            return self._response(request, activation_msg, success=False)

        login(request, user)
        return_url = request.session.pop("return_url", "/")
        return self._response(request, "Login successful", success=True, redirect_url=return_url)

    def _response(self, request, message, success=True, redirect_url=None):
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
            if success and redirect_url:
                response_data["redirect_url"] = redirect_url
            return JsonResponse(response_data, status=200 if success else 400)

        if success:
            messages.success(request, message)
            return redirect(redirect_url or "/")
        else:
            messages.error(request, message)
            return redirect("login")

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
