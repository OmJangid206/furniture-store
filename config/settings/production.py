import os
from .base import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
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
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
