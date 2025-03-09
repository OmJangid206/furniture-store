import requests
from django.core.mail import send_mail
from django.conf import settings
from six import text_type
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def send_forget_password_mail(email, token):
    """
    Sends a password reset email with a reset link.

    Args:
        email (str): The recipient's email address.
        token (str): The unique token for resetting the password.
    """
    subject = "Reset Your Password"
    message = f"Hi, click the link below to reset your password:\n\n" \
              f"http://127.0.0.1:8000/change-password/{token}/"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    # Disable SSL certificate verification (for local testing only)
    requests.post("http://127.0.0.1:8000/forget-password/", verify=False)

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
 