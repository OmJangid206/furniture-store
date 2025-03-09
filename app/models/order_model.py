"""
models/order_model.py

This module defines the `OrderModel` class representing an order placed by a user, 
along with its associated attributes, methods, and relationships with other models.

The `OrderModel` contains information about the user who placed the order, the 
shipping address, payment details, order status, and timestamps. 

This module also includes the `OrderItem` class, which represents individual items 
within an order, including product details, price, and quantity.

Models:
    - OrderModel: Represents an order with user information, shipping details, 
      payment, and order status.
    - OrderItem: Represents an item within an order, containing details of the product, 
      quantity, and price.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class OrderModel(models.Model):
    """
    Represents an order placed by a user within the system.

    This model holds the essential information regarding an order such as 
    user details, shipping address, order status, and payment information.

    Attributes:
        user (ForeignKey): The user who placed the order.
        fname (CharField): The first name of the user.
        lname (CharField): The last name of the user.
        email (CharField): The email of the user.
        phone (CharField): The phone number of the user.
        address (TextField): The delivery address for the order.
        city (CharField): The city of the delivery address.
        state (CharField): The state of the delivery address.
        country (CharField): The country of the delivery address.
        pincode (CharField): The postal code of the delivery address.
        total_price (FloatField): The total price of the order.
        payment_mode (CharField): The mode of payment (e.g., Credit Card, PayPal).
        payment_id (CharField): The unique identifier for the payment.
        status (CharField): The current order status (Pending, Out For Shipping, Completed, Cancelled).
        message (TextField): A custom message associated with the order.
        tracking_number (CharField): The tracking number of the order.
        created_at (DateTimeField): The timestamp when the order was created.
        updated_at (DateTimeField): The timestamp when the order was last updated.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, default="", null=False)
    lname = models.CharField(max_length=150, default="", null=False)
    email = models.CharField(max_length=150, default="", null=False)
    phone = models.CharField(max_length=150, default="", null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, default="", null=False)
    state = models.CharField(max_length=150, default="", null=False)
    country = models.CharField(max_length=150, default="", null=False)
    pincode = models.CharField(max_length=150, default="", null=False)
    total_price = models.FloatField(default=0.0, null=False)
    payment_mode = models.CharField(max_length=150, default="", null=False)
    payment_id = models.CharField(max_length=250, null=True)
    
    orderstatuses = (
        ("Pending", "Pending"),
        ("Out For Shipping", "Out For Shipping"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=150, choices=orderstatuses, default="Pending")
    message = models.TextField(null=True)
    tracking_number = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name_plural = "Orders" 

    def __str__(self):
        """
        Returns a string representation of the OrderModel instance.

        The string includes the order ID and the tracking number.

        Returns:
            str: A string representation of the order.
        """
        return f"{self.id} - {self.tracking_number}"
