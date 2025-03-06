from django.shortcuts import render, redirect
from django.contrib.auth import logout
from app.models.contact_model import ContactModel, FeedbackModel, ServiceModel
from app.models.product_model import ProductModel, CategorieModel
from app.models.profile_model import ProfileModel

from django.views import View
from app.templatetags.cart import total_cart_price
from app import utils
