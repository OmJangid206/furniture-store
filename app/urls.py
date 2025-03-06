from django.urls import path
from .views.home_view import home, product 
from .views.cart_view import cart
from .views.contact_view import contact, feedback, service, about
from .views.profile_view import Login, profile, logout_user, signup, updateprofile,activate
from .views.orders_view import order_view, orderview,cancel_order
from .views.checkout_view import razorpaycheck, placeorder, checkout
from .views.resetPassword import changepassword, forgetpassword
from .middlewares.auth_middlewares import auth_middleware
from .models.product_model import ProductManagerModel

urlpatterns = [
    path("", home.as_view(), name="home"),
    path("about", about, name="about"),
    path("service", service, name="service"),
    path("product", product.as_view(), name="product"),
    path("contact", contact.as_view(), name="contact"),
    path("feedback", auth_middleware(feedback.as_view()), name="feedback"), 
    path("cart", auth_middleware(cart), name="cart"),
    path("signup", signup, name="signup"),
    path("login", Login.as_view(), name="login"),
    path("updateprofile/", updateprofile, name="updateprofile"),
    path("profile/", profile, name="profile"),
    path("orders", order_view, name="orders"),
    path("view-order/<str:t_no>", orderview, name="orderview"),
    path("logout/", logout_user, name="logout"),
    path("forget-password/", forgetpassword, name="forgetpassword"),
    path("change-password/<token>/", changepassword, name="changepassword"),
    path("checkout", auth_middleware(checkout), name="checkout"),
    path("place-order", placeorder, name="placeorder"),
    path("proceed-to-pay", razorpaycheck,),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('search/', ProductManagerModel.search_view, name='search_view'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),

]
