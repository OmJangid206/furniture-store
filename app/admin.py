from django.contrib import admin
from .models.profile_model import ProfileModel
from .models.product_model import ProductModel, CategorieModel
from .models.slider_model import SliderModel
from .models.contact_model import ContactModel, FeedbackModel, ServiceModel
from .models.orders_model import OrderModel, OrderItem
from .models.cart_model import CartModel


# Register your models here.
admin.site.register(ServiceModel)
admin.site.register(CategorieModel)
admin.site.register(ProductModel)
admin.site.register(SliderModel)
admin.site.register(ContactModel)
admin.site.register(FeedbackModel)
admin.site.register(ProfileModel)
admin.site.register(OrderModel)
admin.site.register(CartModel)
admin.site.register(OrderItem)
