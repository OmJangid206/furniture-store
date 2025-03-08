"""
views/contact_view.py

This module defines the `ContactView` class, which handles contact form interactions 
in the application.

It provides functionalities to:
- Render the contact form page.
- Process and store user contact inquiries.

Classes:
    - ContactView: Handles GET and POST requests for the contact page.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from app.models.contact_model import ContactModel
from app.utils.common_utils import get_cart_count


class ContactView(View):
    """
    Handles contact form interactions.

    This view allows users to submit contact inquiries, which are stored in the database.
    The contact page also displays the user's cart count.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests for the contact page.

        Retrieves the user's cart count and renders the contact form.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            HttpResponse: The rendered 'contact.html' page with cart count.
        """
        context = {"cart_count": get_cart_count(request.user)}
        return render(request, "contact.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handles POST requests for contact form submission.

        Extracts user input from the request, saves the contact details, 
        and renders the page with a success message.

        Args:
            request (HttpRequest): The HTTP request instance containing contact form data.

        Returns:
            HttpResponse: The rendered 'contact.html' page with cart count and success message.
        """
        contact = ContactModel(
            name=request.POST.get("name"),
            phone_number=request.POST.get("phone"),
            email=request.POST.get("email"),
            description=request.POST.get("description"),
        )
        contact.save()

        context = {
            "cart_count": get_cart_count(request.user),
            "message": "Thank you for contacting us! We have received your message and will get back to you as soon as possible.",
        }
        return render(request, "contact.html", context)