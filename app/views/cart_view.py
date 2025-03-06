from django.shortcuts import render, redirect
from app.models import ProductModel, CartModel
from app.utils import get_cart_count


def cart(request):
    cart_count = get_cart_count(request.user)
    if request.method == "GET":
        cart_items = CartModel.objects.filter(user=request.user)
        products = [item.product for item in cart_items]
        return render(request,"cart.html",{"products": products, "cart_items": cart_items, "cart_count": cart_count},)

    elif request.method == "POST":
        product_id = request.POST.get("product")
        action = request.POST.get("action")

        if product_id:
            product = ProductModel.objects.get(pk=product_id)
            cart_item = CartModel.objects.filter(user=request.user, product=product).first()
            if action == "remove":
                cart_item.delete()
            elif action == "add":
                cart_item.product_qty += 1
                cart_item.save()
            elif action == "subtract":
                if cart_item.product_qty > 1:
                    cart_item.product_qty -= 1
                    cart_item.save()

        return redirect("cart")
