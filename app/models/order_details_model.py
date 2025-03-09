"""
models/order_details_model.py

This module defines the `OrderDetailsModel` class, which represents an individual product 
in an order, along with the relevant attributes, methods, and relationships.

Each `OrderDetailsModel` is linked to a specific `OrderModel` and `ProductModel`, containing 
details about the product, its price, quantity, and image URL.

Models:
    - OrderDetailsModel: Represents an item within an order, associated with a product, 
      price, quantity, and product image URL.
"""

from django.db import models
from .product_model import ProductModel
from .order_model import OrderModel

class OrderDetailsModel(models.Model):
    """
    Represents an individual item within an order.

    Each `OrderDetailsModel` is associated with a particular `OrderModel` and `ProductModel`,
    and contains information about the product, its price, and the quantity ordered.

    Attributes:
        order (ForeignKey): The order that this item belongs to.
        product (ForeignKey): The product associated with this order item.
        price (FloatField): The price of the product in this order.
        quantity (IntegerField): The quantity of the product in the order.
        product_image_url (URLField): The URL of the product image.
    """

    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=False, default=0)
    product_image_url = models.URLField(null=True)

    class Meta:
        verbose_name_plural = "Order Details" 

    def get_product_image_url(self):
        """
        Retrieves the URL of the product image for this order item.

        If the product associated with this order item has an image, the URL is returned.

        Returns:
            str: The product image URL, or None if no image exists.
        """
        return self.product.image.url if self.product.image else None

    def __str__(self):
        """
        Returns a string representation of the OrderDetailsModel instance.

        The string includes the order ID and the associated tracking number.

        Returns:
            str: A string representation of the order item.
        """
        return f"{self.order.id} - {self.order.tracking_number}"
