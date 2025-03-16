"""
module/product_model.py

This module defines the `ProductModel`, which represents products in an e-commerce system.

Features:
- Stores product details such as name, price, category, description, and image.
- Provides utility methods for retrieving products by ID, category, and search queries.

Classes:
- ProductModel: A Django model for storing product information.
"""

from django.db import models
from django.db.models import Q
from .category_model import CategoryModel
from cloudinary.models import CloudinaryField

class ProductModel(models.Model):
    """
    A Django model representing a product in the system.

    Attributes:
        name (CharField): The name of the product (max length: 50).
        price (IntegerField): The price of the product (default: 0).
        category (ForeignKey): A foreign key linking the product to a category.
        description (TextField): A text description of the product.
        image (ImageField): An image associated with the product.
    """
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, default="", null=True, blank=True
    )
    description = models.TextField()
    image = CloudinaryField('products')

    class Meta:
        db_table = "product"
        verbose_name_plural = "Products" 

    @staticmethod
    def get_all_products_by_id(ids):
        """
        Retrieves products based on a list of product IDs.

        Args:
            ids (list[int]): A list of product IDs.

        Returns:
            QuerySet: A queryset containing matching products.
        """
        return ProductModel.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        """
        Retrieves all products.

        Returns:
            QuerySet: A queryset containing all products.
        """
        return ProductModel.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        """
        Retrieves products based on a specific category ID.

        Args:
            category_id (int): The ID of the category.

        Returns:
            QuerySet: A queryset containing products of the given category.
        """
        if category_id:
            return ProductModel.objects.filter(category=category_id)
        return ProductModel.get_all_products()

    @staticmethod
    def search_products(query):
        """
        Searches for products by name or description.

        Args:
            query (str): The search term.

        Returns:
            QuerySet: A queryset containing products that match the search query.
        """
        if query:
            # Search for products that contain the query string in their name or description
            return ProductModel.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        # Return all products if no query is provided
        return ProductModel.objects.all()


    def __str__(self):
        """
        Returns a string representation of the product manager.

        Returns:
            str: A readable identifier of the class instance.
        """
        return self.name
