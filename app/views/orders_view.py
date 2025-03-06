from django.shortcuts import render
from app.models.orders_model import OrderModel, OrderItem
from django.contrib.auth.decorators import login_required
from app.utils import get_cart_count
from app.middlewares.auth_middlewares import auth_middleware
from django.contrib import messages
from django.shortcuts import redirect


# @auth_middleware
@login_required(login_url="login")
def order_view(request):
    # Calculate cart count
    cart_count = get_cart_count(request.user)

    orders = OrderModel.objects.filter(user=request.user)
    context = {"orders": orders, "cart_count": cart_count}
    return render(request, "orders.html", context)


@login_required(login_url="login")
def orderview(request, t_no):
    # Calculate cart count
    cart_count = get_cart_count(request.user)

    order = OrderModel.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    order_items = OrderItem.objects.filter(order=order)
    context = {"order": order, "orderitems": order_items, "cart_count": cart_count}
    return render(request, "view-order.html", context)


@login_required(login_url="login")
def cancel_order(request, order_id):
    try:
        order = OrderModel.objects.get(id=order_id, user=request.user)
    except OrderModel.DoesNotExist:
        messages.error(request, "Order does not exist.")
        return redirect("order_view")

    if order.status == "Completed":
        messages.error(
            request, "The order has already been completed and cannot be cancelled."
        )
    elif order.status == "Cancelled":
        messages.error(request, "The order has already been cancelled.")
    else:
        order.status = "Cancelled"
        order.save()
        OrderItem.objects.filter(order=order).update(
            status="Cancelled"
        ) 
        messages.success(request, "Order has been successfully cancelled.")

    return redirect("order_view")


@login_required(login_url="login")
def cancel_order(request, order_id):
    try:
        order = OrderModel.objects.get(id=order_id, user=request.user)
    except OrderModel.DoesNotExist:
        messages.error(request, "Order does not exist.")
        return redirect("order_view")

    if order.status == "Completed":
        messages.error(
            request, "The order has already been completed and cannot be cancelled."
        )
    elif order.status == "Cancelled":
        messages.error(request, "The order has already been cancelled.")
    else:
        order.status = "Cancelled"
        order.save()
        messages.success(request, "Order has been successfully cancelled.")

    return redirect("orders")
