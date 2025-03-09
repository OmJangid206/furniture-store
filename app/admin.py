"""
admin.py

Django Admin Model Registrations

This module registers the application's models with the Django admin interface, 
allowing administrators to manage database records through the Django admin panel.

Registered Models:
- ProfileModel
- ProductModel
- CategoryModel
- SliderModel
- ContactModel
- FeedbackModel
- ServiceModel
- OrderModel
- OrderDetailsModel
- CartModel

Usage:
    The registered models will be accessible in the Django Admin Panel.
"""

from django.contrib import admin

# Import models from the current app
from .models.profile_model import ProfileModel
from .models.product_model import ProductModel
from .models.category_model import CategoryModel
from .models.slider_model import SliderModel
from .models.contact_model import ContactModel
from .models.feedback_model import FeedbackModel
from .models.service_model import ServiceModel
from .models.order_model import OrderModel
from .models.order_details_model import OrderDetailsModel
from .models.cart_model import CartModel

# Register models to make them available in the Django Admin Panel
admin.site.register(ProfileModel)
admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(SliderModel)
admin.site.register(ContactModel)
admin.site.register(FeedbackModel)
admin.site.register(ServiceModel)
admin.site.register(OrderModel)
admin.site.register(OrderDetailsModel)
admin.site.register(CartModel)
