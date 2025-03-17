from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
# ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".vercel.app"]


# Email settings
# For local development, use the console email backend (prints emails to console)
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
