from datetime import timedelta
import dj_database_url
from .base import *
import os


DEBUG = False
ALLOWED_HOSTS = ['myecommerce-prod-5f9afe067cf5.herokuapp.com']

SECRET_KEY = os.environ['SECRET_KEY']
USE_TZ = False
ROOT_URLCONF = 'ecommerce.urls'

DATABASES = {
    'default': dj_database_url.config()
}


EMAIL_BACKEND =  os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT'] 

REDIS_URL = os.environ['REDIS_URL']


CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": timedelta(minutes=10),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


