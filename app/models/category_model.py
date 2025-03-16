"""
model/category_model.py

This module defines the CategoryModel, which represents product categories.

Features:
- Stores product category names.
- Provides a method to retrieve all available categories.
"""

from django.db import models


class CategoryModel(models.Model):
    """
    Represents a product category.

    Attributes:
        name (str): The name of the category (max length: 50).
    """
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"
        verbose_name_plural = "Categories"

    @staticmethod
    def get_all_categories():
        """
        Retrieves all available product categories.

        Returns:
            QuerySet: A queryset containing all CategoryModel instances.
        """
        return CategoryModel.objects.all()

    def __str__(self):
        """
        Returns a readable representation of the category.

        Returns:
            str: The name of the category.
        """
        return self.name