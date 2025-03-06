from django.shortcuts import render, redirect
from app.models.product_model import ProductModel, CategorieModel
from app.models.slider_model import SliderModel
from app.models import CartModel
from django.views import View
from app.utils import get_cart_count  


# Home
class home(View):
    def get(self, request):
        products = ProductModel.get_all_products()
        slider = SliderModel.get_all_slider()
        cart_count = get_cart_count(request.user)  # Calculate cart count
        data = { "sliders": slider, "products": products, "cart_count": cart_count }
        return render(request, "home.html", data)

    def post(self, request):
        if request.user.is_authenticated:
            product_id = request.POST.get("product")
            remove = request.POST.get("remove")
            if product_id:
                product = ProductModel.objects.get(pk=product_id)
                user_cart, created = CartModel.objects.get_or_create(user=request.user, product=product)
                if remove:
                    if user_cart.product_qty <= 1:
                        user_cart.delete()
                    else:
                        user_cart.product_qty -= 1
                        user_cart.save()
                else:
                    user_cart.product_qty += 1
                    user_cart.save()
            return redirect("home")
        else:
            return redirect("login") 

# Product
class product(View):
    def get(self, request):
        products = ProductModel.objects.all()
        categories = CategorieModel.objects.all()
        category_id = request.GET.get("category")
        if category_id:
            products = ProductModel.objects.filter(category_id=category_id)
        cart_count = get_cart_count(request.user)  # Calculate cart count
        context = {"products": products, "categories": categories, "cart_count": cart_count}
        return render(request, "product.html", context)

    def post(self, request):
        if request.user.is_authenticated:
            product_id = request.POST.get("product")
            remove = request.POST.get("remove")
            if product_id:
                product = ProductModel.objects.get(pk=product_id)
                user_cart, created = CartModel.objects.get_or_create(user=request.user, product=product)
                if remove:
                    if user_cart.product_qty <= 1:
                        user_cart.delete()
                    else:
                        user_cart.product_qty -= 1
                        user_cart.save()
                else:
                    user_cart.product_qty += 1
                    user_cart.save()
            return redirect("product")
        else:
            return redirect("login")  
