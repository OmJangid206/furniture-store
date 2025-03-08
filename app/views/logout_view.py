"""
views/auth/logout_view.py

This module defines the `LogoutView` class responsible for handling user logout.

Classes:
    - LogoutView: Handles user logout and redirects to the previous page or login.
"""

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect


class LogoutView(LoginRequiredMixin, View):
    """
    Handles user logout while preserving session redirection.

    Features:
    - Ensures user authentication before logging out.
    - Redirects to the stored return URL if available.
    - Displays a logout success message.
    """

    login_url = "login"  # Redirects unauthenticated users to login

    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        """
        Logs out the user and redirects to the return URL or login page.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            HttpResponseRedirect: Redirects the user to the previous page or login.
        """
        return_url = request.session.pop("return_to", "/")
        logout(request)
        messages.info(request, "You are logged out successfully")
        return redirect(return_url)
