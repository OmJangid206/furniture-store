"""
views/cart_view.py

This module defines the `CartView` class, which manages shopping cart operations 
in the application.

Responsibilities:
- Display the shopping cart and its contents.
- Add, remove, and update product quantities in the cart.

Classes:
    - CartView: Handles GET and POST requests for the shopping cart.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views import View
from app.models.cart_model import CartModel
from app.models.product_model import ProductModel
from app.utils.common_utils import get_cart_count


class CartView(View):
    """
    Handles shopping cart interactions.

    Users can view their cart, add or remove products, and update product quantities.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Retrieves and displays the shopping cart.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            HttpResponse: The rendered 'cart.html' template with cart details.
        """
        cart_items = CartModel.objects.filter(user=request.user)
        context = {
            "products": [item.product for item in cart_items],
            "cart_items": self._get_cart_items(request),
            "cart_count": get_cart_count(request.user),
        }
        return render(request, "cart.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handles shopping cart modifications.

        Allows users to add, remove, or update product quantities in their cart.

        Args:
            request (HttpRequest): The HTTP request instance containing cart update details.

        Returns:
            HttpResponse: Redirects back to the cart page.
        """
        product_id = request.POST.get("product")
        action = request.POST.get("action")

        if product_id and action:
            self._process_cart_action(request, product_id, action)

        return redirect("cart")

    def _get_cart_items(self, request: HttpRequest):
        """
        Retrieves the user's cart items.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            list: A list of cart items associated with the user.
        """
        return CartModel.objects.filter(user=request.user)

    def _process_cart_action(self, request: HttpRequest, product_id: str, action: str):
        """
        Processes cart modifications based on the requested action.

        Args:
            request (HttpRequest): The HTTP request instance.
            product_id (str): The ID of the product being modified.
            action (str): The action to perform ('add', 'remove', 'subtract').
        """
        product = get_object_or_404(ProductModel, pk=product_id)
        cart_item = CartModel.objects.filter(user=request.user, product=product).first()

        if not cart_item:
            return

        action_methods = {
            "remove": self._remove_item,
            "add": self._increase_quantity,
            "subtract": self._decrease_quantity,
        }

        if action in action_methods:
            action_methods[action](cart_item)

    def _remove_item(self, cart_item: CartModel):
        """
        Removes an item from the cart.
        """
        cart_item.delete()

    def _increase_quantity(self, cart_item: CartModel):
        """
        Increases the quantity of a cart item.
        """
        cart_item.product_qty += 1
        cart_item.save()

    def _decrease_quantity(self, cart_item: CartModel):
        """
        Decreases the quantity of a cart item, 
        ensuring it doesn't go below 1.
        """
        if cart_item.product_qty > 1:
            cart_item.product_qty -= 1
            cart_item.save()
