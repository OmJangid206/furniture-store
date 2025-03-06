import random
import string
from app.models import CartModel
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


# Genrate random order_id
def generate_id(length=50):
    key = ""
    for i in range(length):
        key += random.choice(
            string.ascii_lowercase + string.ascii_uppercase + string.digits
        )
    return key


def get_cart_count(user):
    if user.is_authenticated:
        return CartModel.objects.filter(user=user).count()
    return 0


# Token Genrate
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk)
            + text_type(timestamp)
            # text_type(user.profile.signup_confirmation)
        )


generate_token = TokenGenerator()
