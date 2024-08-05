from .base import *
import os


DEBUG = False
ALLOWED_HOSTS = []

SECRET_KEY = os.environ['SECRET_KEY']
USE_TZ = False
ROOT_URLCONF = 'ecommerce.urls'

