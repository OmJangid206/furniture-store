"""
models/user_model.py

Defines `UserModel`, a custom user model extending Django's `AbstractUser`.

Features:
- Uses email as the unique identifier.
- Generates a UUID as the primary key.
- Auto-sets username from email if not provided.

Classes:
- UserModel: Custom user model with email-based authentication.
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .user_manager_model import UserManagerModel 

class UserModel(AbstractUser):
    """
    A custom user model that extends Django's `AbstractUser` to use email-based authentication.

    This model modifies the default Django user system by:
    - Using `email` instead of `username` for authentication.
    - Assigning a unique UUID (`uid`) as the primary key.
    - Automatically setting `email` as `username` if `username` is empty.

    Attributes:
        uid (UUIDField): A universally unique identifier (UUID) for each user (Primary Key).
        email (EmailField): A unique and required email address for user authentication.
        username (CharField): A username field (optional, auto-filled with email if left blank).

    Meta:
        db_table: Defines the database table name as "user".
        verbose_name_plural: Sets the plural name of the model as "Users".

    Methods:
        save(): Ensures that if `username` is not provided, it defaults to `email`.
    """
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Assign the custom manager
    objects = UserManagerModel()

    def save(self, *args, **kwargs):
        """
        Overrides the default save method.

        If `username` is not set, it assigns the user's email as the username.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta options for the `UserModel`.

        Attributes:
            db_table (str): Specifies the database table name as "user".
            verbose_name_plural (str): Defines the plural name of the model as "Users".
        """
        db_table = "user"
        verbose_name_plural = "Users"
