#!/usr/bin/env python

"""
Django Management Script

This script provides a command-line interface for running administrative tasks 
within a Django project, such as starting the development server, applying 
migrations, and creating Django apps.

Usage:
    python manage.py <command> [options]

Example:
    python manage.py runserver      # Starts the Django development server
    python manage.py migrate        # Applies database migrations

Environment:
    - `DJANGO_SETTINGS_MODULE` is set to `config.settings` to specify 
      the settings module for the project.

Requirements:
    - Django must be installed and available in the Python environment.
    - The script should be executed within an activated virtual environment.
"""

import os
import sys


def main():
    """
    Execute Django administrative tasks.

    This function:
    - Sets the default Django settings module.
    - Imports and executes the Django command-line utility.
    - Handles ImportError if Django is not installed.

    Raises:
        ImportError: If Django is not installed or cannot be found in 
        the Python environment.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Ensure it is installed and available "
            "on your PYTHONPATH. Did you forget to activate the virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
