from datetime import timedelta
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+jlnj6ek%bx$#)v-(x5z)32%+r8srovv=hi742h(@8nic4uu)g'

USE_TZ = False
ROOT_URLCONF = 'ecommerce.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'P@ssword'
    }
}

CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "TIMEOUT": timedelta(minutes=10),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

