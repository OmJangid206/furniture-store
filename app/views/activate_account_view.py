"""
activate_account_view.py - Class-Based View for User Activation

This module provides a class-based view (`ActivateAccountView`) for handling 
user account activation after registration.

Functionality:
1. User Clicks Activation Link
   - A user receives an email with an activation link containing a base64-encoded user ID (`uidb64`) and a token.
   
2. Decode UID and Validate Token
   - The UID is decoded to fetch the corresponding user.  
   - The activation token is checked for validity.

3. Activate User and Log In 
   - If the token is valid, the user's account is activated.  
   - The user is automatically logged in after activation.

4. Response Handling
   - If activation is successful, a success message is displayed, and the user is redirected to the **Thank You** page.  
   - If activation fails, an error message is displayed, and the user is shown the **Activation Failed** page.

Classes:
    - ActivateAccountView (View): Handles GET requests for user activation.

Usage:
- This view should be linked to the activation URL in Django's `urls.py`.
"""

from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render
from django.views import View
from app.utils.common_utils import get_cart_count
from app.utils.common_utils import TokenGenerator


class ActivateAccountView(View):
    """
    Handles user account activation via a class-based view.

    Methods:
        get: Processes the activation token, activates the user, and logs them in.
    """

    def get_user_from_uid(self, uidb64: str) -> User:
        """
        Decodes the base64-encoded UID and retrieves the corresponding user.

        Args:
            uidb64 (str): Base64 encoded user ID.

        Returns:
            User instance if found, otherwise None.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, OverflowError, User.DoesNotExist):
            return None

    def activate_user(self, request: HttpRequest, user: User) -> None:
        """
        Activates the user's account and logs them in.

        Args:
            request (HttpRequest): The HTTP request object.
            user (User): The user instance to be activated.
        """
        user.is_active = True
        user.save()
        login(request, user)

    def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
        """
        Handles the GET request for user activation.

        Args:
            request (HttpRequest): The HTTP request object.
            uidb64 (str): The base64 encoded user ID.
            token (str): The activation token.

        Returns:
            HttpResponse: A rendered response with either a success or failure message.
        """
        user = self.get_user_from_uid(uidb64)

        if user and TokenGenerator().check_token(user, token):
            self.activate_user(request, user)
            messages.success(request, "Registration complete. You are now logged in.")
            cart_count = get_cart_count(request.user)
            return render(request, "thank-you.html", {"cart_count": cart_count})

        messages.error(request, "Activation failed. Invalid or expired token.")
        return render(request, "activation-failed.html")
