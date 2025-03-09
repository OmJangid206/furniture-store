"""
views/home_view.py

This module defines the `HomeView` class responsible for handling homepage 
requests in the application.

It provides functionalities to:
- Display products and sliders on the homepage.
- Handle cart operations (adding and removing products).
- Redirect unauthenticated users to the login page.

Classes:
    - HomeView: Handles homepage display and cart interactions.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from app.models.product_model import ProductModel
from app.models.slider_model import SliderModel
from app.models.cart_model import CartModel
from django.views import View
from app.utils.common_utils import get_cart_count  


class HomeView(View):
    """
    Handles homepage display and cart operations.

    Methods:
    - get(request): Loads homepage with products, sliders, and cart count.
    - post(request): Handles product addition/removal in the cart.
    - _update_cart(user, product_id, remove): Helper method to modify cart contents.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET request to display the homepage.
        Fetches all products, sliders, and cart item count for the current user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Rendered homepage with the provided context.
        """
        # user_cart = CartModel.objects.filter(user=request.user)
        # print(f"Cart for user {request.user}: {list(user_cart)}")  # Debug print

        context = { 
            "sliders": SliderModel.get_all_slider(), 
            "products": ProductModel.get_all_products(),
            # "cart_items": user_cart,  # ✅ Explicitly passing cart items to template
            "cart_count": get_cart_count(request.user) 
        }
        return render(request, "home.html", context)

    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        """
        Handles POST request for cart operations.
        Adds/removes a product from the cart or redirects unauthenticated users to login.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirects to the homepage.
        """
        if not request.user.is_authenticated:
            return redirect("login")
        
        product_id = request.POST.get("product")
        remove_item = request.POST.get("remove")
        
        if product_id:
            self._update_cart(request.user, product_id, remove_item)

        return redirect("home")
 
    def _update_cart(self, user, product_id: int, remove_item: bool) -> None:
        """
        Updates the cart based on user actions.

        If `remove` is set, the product quantity is decreased, and if it reaches zero, 
        the item is removed from the cart. Otherwise, the quantity is increased.

        Args:
            user (User): The logged-in user.
            product_id (int): ID of the product to be added/removed.
            remove_item (bool): Flag indicating whether to remove the product.

        Returns:
            None
        """
        product = ProductModel.objects.get(pk=product_id)
        cart_item, created = CartModel.objects.get_or_create(user=user, product=product)
        
        print(f"Before Update - Product {cart_item.product.id}, Quantity: {cart_item.product_qty}, Created: {created}")
    
        if remove_item:
            if cart_item.product_qty <= 1:
                print(f"Removing product {product_id} from cart")
                cart_item.delete()
            else:
                cart_item.product_qty -= 1
                print(f"Updated Quantity - Product {cart_item.product.id}, Quantity: {cart_item.product_qty}")
                cart_item.save()
        else:
            cart_item.product_qty += 1
            print(f"Updated Quantity - Product {cart_item.product.id}, Quantity: {cart_item.product_qty}")
            cart_item.save()
 