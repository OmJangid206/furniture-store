import os
from .base import *
# from dotenv import load_dotenv
import logging

# load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".vercel.app"]

# database settings (PostgreSQL)
DATABASES['default'] = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ["DB_NAME"],
    "USER": os.environ["DB_USER"],
    "PASSWORD": os.environ["DB_PASSWORD"],
    "HOST": os.environ["DB_HOST"],
    "PORT": os.getenv("DB_PORT", 5432),
    'OPTIONS': {
            'sslmode': 'require',
    },
}

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

logger.info(f"EMAIL_HOST_USER: {EMAIL_HOST_USER}")
logger.info(f"EMAIL_HOST_PASSWORD: {EMAIL_HOST_PASSWORD}")