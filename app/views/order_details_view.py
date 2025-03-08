"""
This module defines the `OrderDetailsView` class, which handles the display of a user's 
order details, including the order items associated with it.

The `OrderDetailsView` retrieves the order and its related items based on the provided 
tracking number and the logged-in user. It then displays the order details along with 
the user's cart count in a rendered HTML response.

Classes:
    - OrderDetailsView: A view that fetches and displays order details for a specific user.

Functions:
    - get: Handles the GET request to display the order and its items based on the tracking number.
"""

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from typing import Optional
from app.models.order_model import OrderModel
from app.models.order_details_model import OrderDetailsModel
from app.utils.common_utils import get_cart_count


class OrderDetailsView(LoginRequiredMixin, View):
    """
    Displays the details of a specific order, including the associated items.

    This view fetches the order and its associated items based on the tracking number
    and displays them along with the cart count for the user.

    Attributes:
        request (HttpRequest): The HTTP request object that contains the data for the request.
        tracking_number (str): The tracking number of the order to retrieve.
        
    Methods:
        get(request, tracking_number): Handles the GET request to fetch and display the order details.
    """
    
    def get(self, request: HttpRequest, tracking_number: str) -> HttpResponse:
        """
        Handles the GET request to display the details of a specific order.

        This method retrieves the order using the provided tracking number and 
        the logged-in user. It also fetches the associated order items and 
        returns a rendered HTML page with the order details.

        Args:
            request: The HTTP request object that contains the data for the request.
            tracking_number: The tracking number of the order to fetch.

        Returns:
            HttpResponse: A rendered HTML response containing the order and its items.
        """
        cart_count: int = get_cart_count(request.user)

        # Fetch the order using the tracking number and the logged-in user
        order: Optional[OrderModel] = OrderModel.objects.filter(tracking_number=tracking_number).filter(user=request.user).first()

        if not order:
            # If the order does not exist, return an error page or message
            return render(request, "order_not_found.html", {"message": "Order not found."})

        # Fetch all the order items associated with the fetched order
        order_item = OrderDetailsModel.objects.filter(order=order)

        # Prepare the context to pass to the template
        context = {
            "order": order,
            "order_item": order_item,
            "cart_count": cart_count
        }

        # Render and return the HTML response
        return render(request, "view-order.html", context)
