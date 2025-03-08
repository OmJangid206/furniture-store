"""
This module defines the `OrderView` class, which allows authenticated users 
to view their orders.

The view retrieves all orders associated with the logged-in user and displays them 
along with the cart count.

Classes:
    - OrderView: Handles displaying the list of user orders.

Functions:
    - get(request: HttpRequest) -> HttpResponse:
        Fetches and displays the logged-in user's orders.
"""

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from app.models.order_model import OrderModel
from app.utils.common_utils import get_cart_count


class OrderView(LoginRequiredMixin, View):
    """
    Handles the display of all orders for the logged-in user.

    This view fetches the orders associated with the user and presents them 
    along with the cart count.

    Attributes:
        request (HttpRequest): The HTTP request object containing user data.

    Methods:
        get(request: HttpRequest) -> HttpResponse:
            Handles the retrieval and rendering of user orders.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles the GET request to display user orders.

        This method retrieves all orders linked to the logged-in user and 
        displays them along with the cart count.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: A rendered HTML response with the user's orders.
        """
        cart_count = get_cart_count(request.user)
        orders = OrderModel.objects.filter(user=request.user)

        context = {"orders": orders, "cart_count": cart_count}
        return render(request, "order.html", context)
