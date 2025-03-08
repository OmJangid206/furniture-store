"""
templatetags/cart.py

Custom template filters for handling cart-related operations in Django templates.

This module provides custom template filters to check if a product is in the cart, 
retrieve cart quantity, compute total price per product, and calculate the total 
cart price dynamically.

Usage:
    {% load cart %}
    {{ product|is_in_cart:cart }}
    {{ product|cart_quantity:cart }}
    {{ product|total_price:cart }}
    {{ products|total_cart_price:cart }}
"""

from django import template

register = template.Library()


@register.filter(name="is_in_cart")
def is_in_cart(product, cart):
    """
    Checks if a given product exists in the cart.

    Args:
        product (ProductModel): The product instance to check.
        cart (QuerySet): The cart containing cart items.

    Returns:
        bool: True if the product is in the cart, False otherwise.
    """
    return any(cart_item.product.id == product.id for cart_item in cart)

@register.filter(name="cart_quantity")
def cart_quantity(product, cart):
    """
    Retrieves the quantity of a specific product in the cart.

    Args:
        product (ProductModel): The product instance to check.
        cart (QuerySet): The cart containing cart items.

    Returns:
        int: The quantity of the product in the cart, or 0 if not found.
    """
    for cart_item in cart:
        if cart_item.product.id == product.id:
            return cart_item.product_qty
    return 0

@register.filter(name="total_price")
def total_price(product, cart):
    """
    Calculates the total price for a specific product in the cart.

    Args:
        product (ProductModel): The product instance.
        cart (QuerySet): The cart containing cart items.

    Returns:
        float: The total price of the product based on its quantity in the cart.
    """
    return product.price * cart_quantity(product, cart)

@register.filter(name="total_cart_price")
def total_cart_price(products, cart):
    """
    Computes the total price of all products in the cart.

    Args:
        products (QuerySet): A queryset of all products in the cart.
        cart (QuerySet): The cart containing cart items.

    Returns:
        float: The total price of all items in the cart.
    """
    return sum(p.price * cart_quantity(p, cart) for p in products)
