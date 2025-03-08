"""
templatetags/custom_filter.py

Custom template filters for formatting and calculations.

This module provides custom template filters to:
- Format numbers as currency with the Indian Rupee symbol (₹).
- Perform multiplication operations in Django templates.

Usage:
    {% load custom_filter %}
    {{ price|currency }}
    {{ quantity|multiply:unit_price }}

Author: [Your Name]
"""

from django import template

register = template.Library()


@register.filter(name="currency")
def currency(number: float) -> str:
    """
    Formats a number as currency with the Indian Rupee (₹) symbol.

    Args:
        number (float): The number to format.

    Returns:
        str: The formatted currency string (e.g., "₹ 1000").
    """
    return f"₹ {number}"


@register.filter(name="multiply")
def multiply(number: float, number1: float) -> float:
    """
    Multiplies two numbers.

    Args:
        number (float): The first number.
        number1 (float): The second number.

    Returns:
        float: The result of multiplying number by number1.
    """
    return number * number1
