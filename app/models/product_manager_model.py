"""
module/product_manager_model.py

This module defines the `ProductManagerModel`, which provides functionalities 
for managing product-related operations such as searching for products.

Features:
- Handles product search functionality based on user input.
- Retrieves products matching a given query.
- Renders search results in a template.

Classes:
- ProductManagerModel: A class with static methods to manage product-related queries.
"""

from django.shortcuts import render
from .product_model import ProductModel


class ProductManagerModel:
    """
    A manager class for handling product-related queries and operations.
    """
    @staticmethod
    def search_view(request):
        """
        Handles the product search functionality.

        Args:
            request (HttpRequest): The incoming HTTP request containing the search query.

        Returns:
            HttpResponse: A rendered template with the search results.

        Functionality:
        - Retrieves the search query from the request parameters.
        - Filters `ProductModel` objects whose names contain the query string.
        - Renders the `search_result.html` template with the filtered products.
        """
        query = request.GET.get("q") # Extract search query from request
        products = ProductModel.objects.filter(name__icontains=query) if query else []
        context = {"products": products, "query": query}
        return render(request, "search_result.html", context)
