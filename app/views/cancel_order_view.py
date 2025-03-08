"""
This module defines the `CancelOrderView` class, which allows authenticated users 
to cancel their orders under specific conditions.

The view ensures that only eligible orders (i.e., not completed or already canceled) 
can be canceled. Upon cancellation, the order status is updated, and the user is redirected 
to the orders page with a success or error message.

Classes:
    - CancelOrderView: Handles the cancellation of user orders.

Functions:
    - post(request: HttpRequest, order_id: int) -> HttpResponseRedirect:
        Processes the order cancellation request and redirects the user accordingly.
"""

from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from app.models.order_model import OrderModel
from app.models.order_details_model import OrderDetailsModel


class CancelOrderView(LoginRequiredMixin, View):
    """
    Handles the cancellation of a specific order if it meets the criteria.

    This view allows authenticated users to cancel their orders if the order is 
    neither completed nor already canceled. It updates the order status and provides 
    user feedback through success or error messages.

    Attributes:
        request (HttpRequest): The HTTP request object containing user data.
        order_id (int): The ID of the order to cancel.

    Methods:
        post(request: HttpRequest, order_id: int) -> HttpResponseRedirect:
            Handles the order cancellation process and redirects to the orders page.
    """

    def post(self, request: HttpRequest, order_id: int) -> HttpResponseRedirect:
        """
        Handles the POST request to cancel an order.

        This method retrieves the order, verifies its status, and updates it 
        if eligible for cancellation. It also updates associated order details 
        and provides feedback messages to the user.

        Args:
            request (HttpRequest): The HTTP request object containing user data.
            order_id (int): The ID of the order to be canceled.

        Returns:
            HttpResponseRedirect: A redirect response to the orders page with 
            a success or error message.
        """
        try:
            # Fetch the order belonging to the logged-in user
            order = OrderModel.objects.get(id=order_id, user=request.user)
        except OrderModel.DoesNotExist:
            messages.error(request, "Order does not exist.")
            return redirect("order_view")

        # Check order status and handle accordingly
        if order.status == "Completed":
            messages.error(request, "The order has already been completed and cannot be canceled.")
        elif order.status == "Cancelled":
            messages.error(request, "The order has already been canceled.")
        else:
            # Update order and order details status to "Cancelled"
            order.status = "Cancelled"
            order.save()
            OrderDetailsModel.objects.filter(order=order).update(status="Cancelled")
            messages.success(request, "Order has been successfully canceled.")

        return redirect("order_view")
