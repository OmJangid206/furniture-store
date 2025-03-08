"""
views/service_view.py

This module defines the `ServiceView` class responsible for handling requests 
to the Services page in the application.

It provides functionalities to:
- Render the Services page.
- Retrieve and display available services.
- Generate unique colors for text and background.
- Display the user's cart count.

Classes:
    - ServiceView: Handles GET requests for the Services page.
"""

import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from app.models.service_model import ServiceModel
from app.utils.common_utils import get_cart_count


class ServiceView(View):
    """
    Handles the rendering of the Services page.

    This view retrieves the available services and generates unique color 
    attributes for each service before rendering the `service.html` template.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests for the Services page.

        Retrieves the available services, assigns a unique hash and colors to each service, 
        and passes the data to the template context.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            HttpResponse: The rendered 'service.html' page with service data and cart count.
        """
        cart_count = get_cart_count(request.user)
        services = ServiceModel.get_all_sevices()
        service_data = []

        for service in services:
            service_name_hash = abs(hash(service.service_name)) % 16777215
            text_color = self._generate_color()
            background_color = self._generate_color()

            service_data.append(
                {
                    "service": service,
                    "service_name_hash": service_name_hash,
                    "text_color": text_color,
                    "background_color": background_color,
                }
            )

        context = {"services": service_data, "cart_count": cart_count}
        return render(request, "service.html", context)

    def _generate_color(self) -> str:
        """
        Generates a random pastel-like color in hexadecimal format.

        Returns:
            str: A hex color code in the format '#RRGGBB'.
        """
        r = random.randint(180, 255)
        g = random.randint(180, 255)
        b = random.randint(180, 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)