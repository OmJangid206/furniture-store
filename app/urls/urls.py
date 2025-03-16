from django.urls import path
from ..views.home_view import HomeView
from ..views.product_view import ProductView 
from ..views.about_view import AboutView
from ..views.service_view import ServiceView
from ..views.contact_view import ContactView
from ..views.feedback_view import FeedbackView
from ..views.cart_view import CartView
from ..views.signup_view import SignUpView
from ..views.login_view import LoginView
from ..views.logout_view import LogoutView
from ..views.profile_view import ProfileView
from ..views.update_profile_view import UpdateProfileView
from ..views.password_view import ChangePasswordView, ForgetPasswordView
from ..views.activate_account_view import ActivateAccountView
from ..views.order_view import OrderView
from ..views.order_details_view import OrderDetailsView
from ..views.cancel_order_view import CancelOrderView
from ..views.search_handler_view import SearchHandlerView
from ..views.checkout_view import CheckoutView, PlaceOrderView, RazorpayCheckView
from ..middlewares.auth_middlewares import auth_middleware


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("product", ProductView.as_view(), name="product"),
    path("about", AboutView.as_view(), name="about"),
    path("service", ServiceView.as_view(), name="service"),
    path("contact", ContactView.as_view(), name="contact"),
    path("feedback", auth_middleware(FeedbackView.as_view()), name="feedback"), 
    path("cart", auth_middleware(CartView.as_view()), name="cart"),
    path("signup", SignUpView.as_view(), name="signup"),
    path('activate_account/<uidb64>/<token>/',ActivateAccountView.as_view(),name='activate_account'),
    path("login", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("update-profile/", UpdateProfileView.as_view(), name="updateprofile"),
    path("forget-password/", ForgetPasswordView.as_view(), name="forgetpassword"),
    path("change-password/<token>/", ChangePasswordView.as_view(), name="changepassword"),
    path("order", OrderView.as_view(), name="order"),
    path("view-order/<str:tracking_number>", OrderDetailsView.as_view(), name="order_view"),
    path('cancel_order/<int:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
    path('search/', SearchHandlerView.search_view, name='search_view'),
    path("checkout", auth_middleware(CheckoutView.as_view()), name="checkout"),
    path("place-order", PlaceOrderView.as_view(), name="placeorder"),
    path("proceed-to-pay", RazorpayCheckView.as_view(), name="razorpay-check"),
]
