"""
This module contains the class-based view for displaying the user's profile.

The `ProfileView` class handles displaying the profile page for authenticated users.
Only users who are logged in can access the profile page.

Classes:
    ProfileView (View): A view for displaying the user's profile with cart count.
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from app.utils.common_utils import get_cart_count


@method_decorator(login_required(login_url="login"), name="dispatch")
class ProfileView(View):
    """
    A class-based view for displaying the user's profile.

    This view renders the profile page with the current cart count for the logged-in user.
    Only authenticated users can access this view.

    Attributes:
        request: The HTTP request object.
    
    Methods:
        get: Handles GET requests and renders the profile page.
    """
    
    def get(self, request: HttpRequest ) -> HttpResponse:
        """
        Handles GET requests to display the profile page with the cart count.

        Args:
            request: The HTTP request object.

        Returns:
            Rendered profile page with the cart count.
        """
        cart_count = get_cart_count(request.user)
        return render(request, "profile.html", {"cart_count": cart_count})
