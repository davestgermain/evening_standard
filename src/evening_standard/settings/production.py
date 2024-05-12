from .base import *

DEBUG = False

ALLOWED_HOSTS = ["eveningstandardjazz.com"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_HOST_USER = "django@pobblelabs.org"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "django@pobblelabs.org"

STATIC_ROOT = "/var/www/htdocs/eveningstandardjazz.com/static/"
MEDIA_ROOT = "/var/www/htdocs/eveningstandardjazz.com/media/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/var/www/evening_standard/db.sqlite3",
    }
}
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": "/var/www/evening_standard/whoosh_index",
    },
}

ADMINS = [("Dave St.Germain", "dcs@pobblelabs.org")]

WAGTAILDOCS_SERVE_METHOD = "redirect"


try:
    from .local import *
except ImportError:
    pass
