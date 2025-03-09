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

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views import View
from app.middlewares.auth_middlewares import unauthentcated_user


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
            HttpResponse: Redirects to `return_url` (if exists), , or login page on failure.
        """
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return_url = request.session.pop("return_url", None)
            return redirect(return_url or "/")  # Redirect to homepage
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")
