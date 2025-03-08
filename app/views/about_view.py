"""
views/about_view.py

This module defines the `AboutView` class responsible for handling requests 
to the About page in the application.

It provides functionalities to:
- Render the About page.
- Display the user's cart count.

Classes:
    - AboutView: Handles GET requests for the About page.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from app.utils.common_utils import get_cart_count


class AboutView(View):
    """
    Handles the rendering of the About page.

    This view retrieves the cart count for the authenticated user and 
    passes it to the template context.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests for the About page.

        Retrieves the cart count for the authenticated user and renders the 
        'about.html' template.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            HttpResponse: The rendered about page with cart count in the context.
        """
        cart_count = get_cart_count(request.user)
        context = {"cart_count": cart_count}
        return render(request, "about.html", context)
