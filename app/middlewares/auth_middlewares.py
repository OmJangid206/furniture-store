"""
auth_middlewares.py - Middleware & Decorator for Authentication Handling

This module enforces authentication rules for accessing views.

Features:
1. auth_middleware (Middleware):
    - Redirects unauthenticated users to the login page, preserving their intended URL.
    - Stores the last visited path for authenticated users.

2. unauthentcated_user (Decorator):
    - Prevents authenticated users from accessing specific views.
    - Redirects them to the home page if already logged in.

### Usage:
- Add `auth_middleware` to Django's `MIDDLEWARE` settings.
- Use `@unauthentcated_user` to prevent logged-in users from accessing specific views.

"""

from django.shortcuts import redirect


def auth_middleware(get_response):
    """
    Middleware to ensure users are authenticated before accessing certain pages.

    - If unauthenticated, the user is redirected to login, and the return URL is stored.
    - If authenticated, their last visited path is saved in the session.

    Args:
        get_response (Callable): The next middleware or view function in the request chain.

    Returns:
        Callable: Middleware function.
    """
    def middleware(request):
        if not request.user.is_authenticated:
            return_url = request.path
            request.session["return_to"] = return_url
            return redirect(f"login?return_url={return_url}")

        request.session["return_to"] = request.path
        return get_response(request)

    return middleware


def unauthentcated_user(view_function):
    """
    Decorator to prevent authenticated users from accessing certain views.

    - Redirects authenticated users to the home page.
    - Allows unauthenticated users to proceed normally.

    Args:
        view_function (Callable): The view function to be wrapped.

    Returns:
        Callable: Decorated view function.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_function(request, *args, **kwargs)

    return wrapper
