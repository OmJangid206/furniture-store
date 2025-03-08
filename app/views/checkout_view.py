"""
views/checkout_view.py

This module contains views related to the checkout and order placement process, 
including handling the checkout page, placing an order, and calculating 
the total price for Razorpay payment processing.

Classes:
    - CheckoutView: Handles the checkout page display for the logged-in user.
    - PlaceOrderView: Processes order placement by creating an order and clearing the cart.
    - RazorpayCheckView: Computes the total cart price for Razorpay payment.
"""

import random
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User

from app.models.profile_model import ProfileModel
from app.models.order_model import OrderModel
from app.models.order_details_model import OrderDetailsModel
from app.models.cart_model import CartModel
from app.utils.common_utils import get_cart_count
from app.templatetags.cart import total_cart_price


class CheckoutView(LoginRequiredMixin, View):
    """
    Handles the checkout process for authenticated users.
    Displays cart items and user profile details.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET request for checkout page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Renders checkout page with cart details.
        """
        cart_count = get_cart_count(request.user)
        cart_items = CartModel.objects.filter(user=request.user)
        user_profile = ProfileModel.objects.filter(user=request.user).first()

        context = {
            "products": [item.product for item in cart_items],
            "user_profile": user_profile,
            "cart_items": cart_items,
            "cart_count": cart_count,
        }
        return render(request, "checkout.html", context)


class PlaceOrderView(LoginRequiredMixin, View):
    """
    Processes order placement by creating an order and clearing the cart.
    """

    def post(self, request: HttpRequest) -> HttpResponse | JsonResponse:
        """
        Handles POST request to place an order.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Redirects to the orders page.
            JsonResponse: Returns success message if payment is via Razorpay.
        """
        current_user = User.objects.filter(id=request.user.id).first()

        # Update user details if missing
        if not current_user.first_name:
            current_user.first_name = request.POST.get("fname")
            current_user.last_name = request.POST.get("lname")
            current_user.save()

        # Create or update user profile
        user_profile, created = ProfileModel.objects.get_or_create(user=request.user)
        user_profile.phone = request.POST.get("phone")
        user_profile.address = request.POST.get("address")
        user_profile.city = request.POST.get("city")
        user_profile.state = request.POST.get("state")
        user_profile.country = request.POST.get("country")
        user_profile.pincode = request.POST.get("pincode")
        user_profile.save()

        # Create new order
        new_order = OrderModel(
            user=request.user,
            fname=request.POST.get("fname"),
            lname=request.POST.get("lname"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            country=request.POST.get("country"),
            pincode=request.POST.get("pincode"),
            payment_mode=request.POST.get("payment_mode"),
            payment_id=request.POST.get("payment_id"),
        )

        cart_items = CartModel.objects.filter(user=request.user)
        new_order.total_price = total_cart_price(
            [item.product for item in cart_items], cart_items
        )

        # Generate unique tracking number
        while True:
            tracking_number = f"krishna{random.randint(1111111, 9999999)}"
            if not OrderModel.objects.filter(tracking_number=tracking_number).exists():
                new_order.tracking_number = tracking_number
                break

        new_order.save()

        # Create order details
        for item in cart_items:
            OrderDetailsModel.objects.create(
                order=new_order,
                product=item.product,
                price=item.product.price,
                quantity=item.product_qty,
            )

        # Clear cart after order placement
        cart_items.delete()

        messages.success(request, "Your order has been placed successfully.")

        if request.POST.get("payment_mode") == "Paid by Razorpay":
            return JsonResponse({"status": "Your order has been placed successfully"})

        return redirect("orders")


class RazorpayCheckView(LoginRequiredMixin, View):
    """
    View to calculate the total price of items in the user's cart 
    for Razorpay payment processing.

    Retrieves all cart items for the logged-in user, computes the total price, 
    and returns it as a JSON response. If the cart is empty, 
    the total price defaults to 0.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """
        Handles GET requests to return the total cart price.

        Args:
            request (HttpRequest): The HTTP request object containing user details.

        Returns:
            JsonResponse: A JSON response containing the total price of cart items.
        """
        cart_items = CartModel.objects.filter(user=request.user)
        total_price = total_cart_price([item.product for item in cart_items], cart_items)

        return JsonResponse({"total_price": total_price})
