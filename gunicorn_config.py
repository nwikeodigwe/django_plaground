import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

bind = '0.0.0.0:8000'
workers = 3
