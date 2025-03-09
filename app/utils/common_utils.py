"""
common_utils.py - General Utility Functions

This module provides a collection of general utility functions used across the application.

Functions:
    generate_id(length=50): Generates a random alphanumeric ID.
    get_cart_count(user): Retrieves the cart item count for a user.
    TokenGenerator: Generates tokens for password reset and email verification.

### Usage:
- Import functions and the TokenGenerator class from this module as needed.
"""

import random
import string
from six import text_type
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from app.models.cart_model import CartModel


def generate_id(length: int = 50) -> str:
    """
    Generates a random order ID.

    Args:
        length (int): The length of the generated ID.

    Returns:
        str: The generated random order ID.
    """
    key = ""
    for _ in range(length):
        key += random.choice(
            string.ascii_lowercase + string.ascii_uppercase + string.digits
        )
    return key

def get_cart_count(user):
    """
    Retrieves the cart item count for a user.

    Args:
        user: The user object.

    Returns:
        int: The number of items in the user's cart.
    """
    if user.is_authenticated:
        return CartModel.objects.filter(user=user).count()
    return 0

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Generates tokens for password reset and email verification.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Generates a hash value for the token.

        Args:
            user: The user object.
            timestamp: The timestamp of token generation.

        Returns:
            str: The hash value.
        """
        return text_type(user.pk) + text_type(timestamp)
 