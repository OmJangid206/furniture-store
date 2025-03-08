"""
signals/user_signals.py - 

Django Signals for User Profile Creation

This module listens for Django model events and performs automated actions. 
It ensures that a `ProfileModel` instance is created whenever a new `User` is registered.

Signals:
- `create_user_profile`: Automatically creates a `ProfileModel` for new users.

Usage:
Ensure this file is imported in the `ready` method of your `apps.py` to activate the signal.

"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models.profile_model import ProfileModel


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a ProfileModel when a new User is registered.

    - If a User instance is newly created, this function ensures a 
      corresponding ProfileModel instance exists.

    Args:
        sender (Model): The model class sending the signal.
        instance (User): The instance of the User model being saved.
        created (bool): Whether this is a new User instance.
        **kwargs: Additional keyword arguments.

    """
    if created:
        ProfileModel.objects.get_or_create(user=instance)
