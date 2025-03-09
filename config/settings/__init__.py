import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "production")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "development":
    from .development import *
