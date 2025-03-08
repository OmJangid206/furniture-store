"""
models/contact_model.py

This module defines the `ContactModel` class, which represents contact inquiries 
submitted through the application.

It provides functionalities to:
- Store user contact details, including name, phone number, email, and description.
- Retrieve contact information.

Classes:
    - ContactModel: Represents a contact inquiry entry.
"""

from django.db import models


class ContactModel(models.Model):
    """
    Represents a contact inquiry in the application.

    Attributes:
        name (str): The name of the user submitting the inquiry (max length: 50 characters).
        phone_number (str): The user's phone number (max length: 15 characters).
        email (str): The email address of the user.
        description (str): The message or inquiry details provided by the user.
    """
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        """
        Returns a string representation of the contact entry.

        Returns:
            str: The name of the user who submitted the contact inquiry.
        """
        return self.name
