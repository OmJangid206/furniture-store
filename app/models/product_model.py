from django.db import models
from django.db.models import Q
from django.shortcuts import render


# Product Categorires
class CategorieModel(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return CategorieModel.objects.all()

    def __str__(self):
        return self.name


# Product
class ProductModel(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(CategorieModel, on_delete=models.CASCADE, default="", null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="products/")

    @staticmethod
    def get_all_products_by_id(ids):
        return ProductModel.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return ProductModel.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return ProductModel.objects.filter(category=category_id)
        else:
            return ProductModel.get_all_products()

    @staticmethod
    def search_products(query):
        if query:
            # Search for products that contain the query string in their name or description
            return ProductModel.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        else:
            # Return all products if no query is provided
            return ProductModel.objects.all()


class ProductManagerModel:
    @staticmethod
    def search_view(request):
        query = request.GET.get("q")
        products = ProductModel.objects.filter(name__icontains=query) if query else []
        context = {"products": products, "query": query}
        return render(request, "search_result.html", context)

    def __str__(self):
        return self.name
