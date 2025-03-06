from django.db import models
from .product_model import ProductModel
from django.contrib.auth.models import User
from django.utils import timezone


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
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
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return "{} - {}".format(self.id, self.tracking_no)


class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=False, default=0)
    # product_image = models.URLField(null=True)
    product_image_url = models.URLField(null=True)

    def get_product_image_url(self):
        return self.product.image.url if self.product.image else None

    def __str__(self):
        return "{} - {}".format(self.order.id, self.order.tracking_no)
