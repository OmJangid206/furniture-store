"""
view/search_handler_view.py

This module provides a class for managing product-related operations,
such as searching for products based on user input.

Features:
- Retrieves products matching a given query.
- Renders search results in a template.

Classes:
- SearchHandlerView: A class with static methods for managing product search functionality.
"""

from django.shortcuts import render
from app.models.product_model import ProductModel


class SearchHandlerView:
    """
    A class for managing product search operations.
    """

    @staticmethod
    def search_products(query):
        """
        Filters products based on a search query.

        Args:
            query (str): The search term.

        Returns:
            QuerySet: A queryset containing matching products.
        """
        return ProductModel.objects.filter(name__icontains=query) if query else ProductModel.objects.none()

    @staticmethod
    def search_view(request):
        """
        Handles the product search functionality and renders search results.

        Args:
            request (HttpRequest): The incoming HTTP request containing the search query.

        Returns:
            HttpResponse: A rendered template with the search results.
        """
        query = request.GET.get("q", "").strip()
        products = SearchHandlerView.search_products(query)
        context = {"products": products, "query": query}
        return render(request, "search-result.html", context)
