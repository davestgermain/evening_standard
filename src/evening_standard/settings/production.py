from .base import *

DEBUG = False

ALLOWED_HOSTS = ["eveningstandardjazz.com"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "naquag.forum@gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "naquag.forum@gmail.com"

STATIC_ROOT = "/data/www/eveningstandardjazz.com/static/"
MEDIA_ROOT = "/data/www/eveningstandardjazz.com/media/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/www/eveningstandardjazz.com/db.sqlite3",
    }
}
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": "/data/www/eveningstandardjazz.com/whoosh_index",
    },
}

ADMINS = [("Dave St.Germain", "dave@st.germa.in")]

WAGTAILDOCS_SERVE_METHOD = "redirect"


try:
    from .local import *
except ImportError:
    pass
