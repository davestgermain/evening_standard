from .base import *

DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = ["eveningstandardjazz.com"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
# EMAIL_HOST_USER = "django@pobblelabs.org"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
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

CACHES["default"] =  {
    'BACKEND': 'django_redis.cache.RedisCache',
    "LOCATION": "redis://127.0.0.1:6379/1",
    'OPTIONS': {
        'CLIENT_CLASS': 'django_redis.client.DefaultClient',
    }
}

ADMINS = [("Dave St.Germain", "dcs@pobblelabs.org")]

WAGTAILDOCS_SERVE_METHOD = "redirect"


try:
    from .local import *
except ImportError:
    pass
