"""
models/user_manager_model.py

Defines `UserManager`, a custom manager for `UserModel` to support email-based authentication.

Features:
- Ensures user creation with email as the unique identifier.
- Supports creating both regular users and superusers.
"""

from django.contrib.auth.models import BaseUserManager

class UserManagerModel(BaseUserManager):
    """
    Custom manager for the `UserModel` to enable email-based authentication.

    This manager provides methods to create both regular users and superusers
    without requiring a username.

    Methods:
        create_user(email, password=None, **extra_fields):
            Creates and returns a regular user with an email identifier.
        
        create_superuser(email, password=None, **extra_fields):
            Creates and returns a superuser with all admin privileges.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user using email as the unique identifier.

        Args:
            email (str): The user's email address (required).
            password (str, optional): The user's password. Defaults to None.
            **extra_fields: Additional fields to be stored in the user model.

        Returns:
            UserModel: The created user instance.

        Raises:
            ValueError: If the email field is not provided.
        """
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password before saving
        user.save(using=self._db)  # Saves the user to the default database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with all admin permissions.

        This method ensures that the superuser has the `is_staff` and `is_superuser`
        flags set to True.

        Args:
            email (str): The superuser's email address.
            password (str, optional): The superuser's password. Defaults to None.
            **extra_fields: Additional fields to be stored in the user model.

        Returns:
            UserModel: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)
