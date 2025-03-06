from django.shortcuts import render, redirect
from app.templatetags.cart import total_cart_price
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from app.models.profile_model import ProfileModel
from django.http import JsonResponse
from app.models.orders_model import OrderModel, OrderItem
from django.conf import settings
from django.contrib import messages
from app.models import CartModel
from app.utils import get_cart_count
import random


@login_required(login_url="login")
def checkout(request):
    if request.method == "GET":
        cart_count = get_cart_count(request.user)
        cart_items = CartModel.objects.filter(user=request.user)
        products = [item.product for item in cart_items]
        userprofile = ProfileModel.objects.filter(user=request.user).first()
        context = {
            "products": products,
            "userprofile": userprofile,
            "cart_items": cart_items,
            "cart_count": cart_count,
        }
        return render(request, "checkout.html", context)


@login_required(login_url="login")
def placeorder(request):
    if request.method == "POST":
        cart_count = get_cart_count(request.user)
        # Update user's first name and last name if they are not already set
        currentuser = User.objects.filter(id=request.user.id).first()
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get("fname")
            currentuser.last_name = request.POST.get("lname")
            currentuser.save()

        # Check if the user has a profile, and create/update it accordingly
        if not ProfileModel.objects.filter(user=request.user):
            userprofile = ProfileModel()
            userprofile.user = request.user
            userprofile.phone = request.POST.get("phone")
            userprofile.address = request.POST.get("address")
            userprofile.city = request.POST.get("city")
            userprofile.state = request.POST.get("state")
            userprofile.country = request.POST.get("country")
            userprofile.pincode = request.POST.get("pincode")
            userprofile.save()

        # Create a new order
        neworder = OrderModel()
        neworder.user = request.user
        neworder.fname = request.POST.get("fname")
        neworder.lname = request.POST.get("lname")
        neworder.email = request.POST.get("email")
        neworder.phone = request.POST.get("phone")
        neworder.address = request.POST.get("address")
        neworder.city = request.POST.get("city")
        neworder.state = request.POST.get("state")
        neworder.country = request.POST.get("country")
        neworder.pincode = request.POST.get("pincode")
        neworder.payment_mode = request.POST.get("payment_mode")
        neworder.payment_id = request.POST.get("payment_id")

        # Retrieve cart items from the database
        cart_items = CartModel.objects.filter(user=request.user)
        products = [item.product for item in cart_items]
        cart_total_price = total_cart_price(products, cart_items)

        neworder.total_price = cart_total_price

        trackno = "krishna" + str(random.randint(1111111, 9999999))
        while OrderModel.objects.filter(tracking_no=trackno) is None:
            trackno = "krishna" + str(random.randint(1111111, 9999999))
        neworder.tracking_no = trackno
        neworder.save()

        # Create order items
        neworderitems = CartModel.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.product_qty,
            )

        CartModel.objects.filter(user=request.user).delete()
        messages.success(request, "Your order has been placed successfully")

        payMode = request.POST.get("payment_mode")
        if payMode == "Paid by Razorpay":
            return JsonResponse({"status": "Your order has been placed successfully"})

    messages.success(request, "Your order has been placed successfully")
    return redirect("orders")


def razorpaycheck(request):
    user = request.user
    cart_items = CartModel.objects.filter(user=user)
    products = [item.product for item in cart_items]
    cart_total_price = total_cart_price(products, cart_items)
    print(cart_total_price)
    return JsonResponse({"total_price": cart_total_price})
