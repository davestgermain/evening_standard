from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-pgd!4@rupt-k6)^u(-&&m%cllvy3fi$*gkwhi5aqb9q=kw8#ib"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += [
    "django_watchfiles",
]

try:
    from .local import *
except ImportError:
    pass
