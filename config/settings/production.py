from .base import *

DEBUG = False
ALLOWED_HOSTS = [".vercel.app"]

# database settings (PostgreSQL)
# DATABASES['default'] = {
#     "ENGINE": "django.db.backends.postgresql",
#     "NAME": os.environ["DB_NAME"],
#     "USER": os.environ["DB_USER"],
#     "PASSWORD": os.environ["DB_PASSWORD"],
#     "HOST": os.environ["DB_HOST"],
#     "PORT": os.environ["DB_PORT"],
# }

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
