from pathlib import Path
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parents[2]  # Moves up 2 levels

# SECRET_KEY is used to provide cryptographic signing.
# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# INSTALLED_APPS lists all the enabled Django apps in the project.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    "cloudinary",
    "cloudinary_storage",
]

# MIDDLEWARE lists classes that process requests and responses in Django.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ROOT_URLCONF points to the module where the URL configurations are defined.
# It tells Django where to look for URL patterns.
ROOT_URLCONF = "config.urls"

# TEMPLATES defines settings for the template system used in Django.
# It specifies the template backend, directories to look for templates, and context processors.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "app", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Default database settings (SQLite)
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# WSGI_APPLICATION points to the WSGI app used to serve the app in production.
# It defines how Django interacts with the web server to handle requests.
WSGI_APPLICATION = "config.wsgi.application"

# AUTH_PASSWORD_VALIDATORS is a list of validators to enforce password security
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Language and timezone settings for the project.
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# STATIC_URL defines the URL path where static files (like CSS, JavaScript, and images) will be served from.
# STATICFILES_DIRS defines the locations of the static files on the file system.
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "app/static")]

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.environ["CLOUD_NAME"],
    api_key=os.environ["CLOUDINARY_API_KEY"],
    api_secret=os.environ["CLOUDINARY_API_SECRET"],
    secure=True
)

# Cloudinary as Default Media Storage
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
MEDIA_URL = f"https://res.cloudinary.com/{os.getenv('CLOUD_NAME')}/"

# Media files (uploads)
# MEDIA_URL defines the URL path where media files (like images, documents, etc.) will be served from.
# MEDIA_ROOT defines the file system path where media files will be stored.
# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# DEFAULT_AUTO_FIELD specifies the default field type for auto-incrementing primary keys.
# By default, Django uses an AutoField (integer) for primary keys. Setting this to BigAutoField
# uses a larger integer (BigInteger) for cases where you expect a very large number of records.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SECURE_CROSS_ORIGIN_OPENER_POLICY controls the security of window.opener when opening a new window.
# `same-origin-allow-popups` allows popups but restricts cross-origin access for security.
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
