"""
Module: app/apps.py

This module defines the configuration for the 'app' Django application.

It includes the application's configuration class, `MyAppConfig`, which
specifies the default auto field and the application's name. It also
overrides the `ready` method to import signal handlers when the application
is ready.

Classes:
    MyAppConfig: Configuration class for the 'app' application.
"""

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    """
    Configuration class for the 'app' Django application.

    This class extends the base `AppConfig` class from Django and provides
    specific configuration settings for the 'app' application.

    Attributes:
        default_auto_field (str): The default type of auto-generated primary
                                  key used for models in this application.
                                  Set to "django.db.models.BigAutoField".
        name (str): The name of the application, set to "app".
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        """
        Called when the application is ready.

        This method is overridden to import the signal handlers for the
        'app' application. This ensures that signals are registered and
        connected when the application starts.
        """
        import app.signals.user_signals
