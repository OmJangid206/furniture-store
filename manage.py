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

Functionality:
    - `execute_from_command_line(sys.argv)`: This function takes command-line 
      arguments and runs the corresponding Django management command.
      It is responsible for handling commands like `runserver`, `migrate`, 
      `createsuperuser`, and more.

    Example:
        If the script is run with:
        ```bash
        python manage.py runserver 8080
        ```
        Then, internally, the function is called as:
        ```python
        execute_from_command_line(["manage.py", "runserver", "8080"])
        ```
        This starts the Django development server on port 8080.
"""

import os
import sys
import traceback
from django.core.management import execute_from_command_line

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
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        sys.stderr.write(
            "Couldn't import Django. Ensure it is installed and available "
            "on your PYTHONPATH. Did you forget to activate the virtual environment?"
        )
        sys.stderr.write(traceback.format_exc())
        sys.exit()

if __name__ == "__main__":
    main()
