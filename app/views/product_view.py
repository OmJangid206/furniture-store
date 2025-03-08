"""
views/product_view.py

This module defines the `ProductView` class responsible for handling productpage 
requests in the application.

It provides functionalities to:
- Display products on the productpage.
- Handle cart operations (adding and removing products).
- Redirect unauthenticated users to the login page.

Classes:
    - ProductView: Handles productpage display and cart interactions.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from app.models.product_model import ProductModel
from app.models.category_model import CategoryModel
from app.models.cart_model import CartModel
from django.views import View
from app.utils.common_utils import get_cart_count 


class ProductView(View):
    """
    Handles productpage display and cart operations.

    Methods:
    - get(request): Loads productpage with products, and cart count.
    - post(request): Handles product addition/removal in the cart.
    - _update_cart(user, product_id, remove): Helper method to modify cart contents.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET request to display products.
        Filters products by category if a category ID is provided.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Rendered product page with products, categories, and cart count.
        """
        category_id = request.GET.get("category")
        products = ProductModel.objects.filter(category_id=category_id) \
            if category_id else ProductModel.objects.all()

        context = {
            "products": products, 
            "categories": CategoryModel.objects.all(), 
            "cart_count": get_cart_count(request.user)
        }
        return render(request, "product.html", context)

    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        """
        Handles POST request for cart operations.
        Adds/removes a product from the cart or redirects unauthenticated users to login.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirects to the productpage.
        """
        if not request.user.is_authenticated:
            return redirect("login")
        
        product_id = request.POST.get("product")
        remove_item = request.POST.get("remove")
        
        if product_id:
            self._update_cart(request.user, product_id, remove_item)

        return redirect("product")

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
        cart_item = CartModel.objects.get_or_create(user=user, product=product)

        if remove_item:
            if cart_item.product_qty <= 1:
                cart_item.delete()
            else:
                cart_item.product_qty -= 1
                cart_item.save()
        else:
            cart_item.product_qty += 1
            cart_item.save()
