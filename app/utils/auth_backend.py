from django.contrib.auth.backends import ModelBackend
from app.models.user_model import UserModel

class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows authentication using email.
    Returns the user even if they are inactive.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate user using email instead of username.

        Args:
            request: The HTTP request object.
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            UserModel or None: The authenticated user or None if authentication fails.
        """
        if email is None or password is None:
            return None
        
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        """
        Retrieve a user using `uid` as the primary key.

        Args:
            user_id (UUID): The user's UUID.

        Returns:
            UserModel or None: The user if found, else None.
        """
        try:
            print(f"get_user() called with user_id: {user_id}")
            return UserModel.objects.get(uid=user_id)
        except UserModel.DoesNotExist:
            return None
