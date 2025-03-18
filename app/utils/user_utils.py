import uuid
import base64
import requests
from django.core.mail import send_mail
from django.conf import settings
from six import text_type
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site


def send_forget_password_mail(request, email, token):
    """
    Sends a password reset email with a reset link.

    Args:
        email (str): The recipient's email address.
        token (str): The unique token for resetting the password.
    """
    current_site = get_current_site(request)
    reset_url = f"{request.scheme}://{current_site.domain}/change-password/{token}/"
    subject = "Reset Your Password"
    message = f"Hi, click the link below to reset your password:\n\n{reset_url}"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    
    # Call the password reset API dynamically using the correct domain
    requests.post(f"{request.scheme}://{current_site.domain}/forget-password/", verify=False)

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

def generate_uuid() -> str:
    """
    Generates a URL-safe, base64-encoded UUID.

    Returns:
        str: A URL-safe, base64-encoded UUID as a string.
    """
    raw_uuid_bytes = uuid.uuid4().bytes
    encoded_uuid = base64.urlsafe_b64encode(raw_uuid_bytes).rstrip(b'=').decode('utf-8')
    return encoded_uuid
