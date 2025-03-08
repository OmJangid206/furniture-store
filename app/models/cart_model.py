"""
model/cart_model.py

This module defines the CartModel, representing a shopping cart system 
where users can add products with specific quantities.

Features:
- Tracks products added to a user's cart.
- Associates each cart item with a user and a product.
- Uses a custom model manager for optimized queries.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .product_model import ProductModel

class CartModel(models.Model):
    """
    Represents a shopping cart item that links a user to a product with a specific quantity.

    Attributes:
        user (User): The user who owns the cart item.
        product (ProductModel): The product added to the cart.
        product_qty (int): The quantity of the product in the cart.
        created_at (datetime): The timestamp when the cart item was added.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, default="", null=True, blank=True
    )
    product_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        """
        Returns a readable representation of the cart item.
        """
        product_name = self.product.name if self.product else "No Product"
        return f"CartItem(user={self.user.username}, product={product_name}, qty={self.product_qty})"
