import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

celery = Celery('ecommerce')
celery.config_from_object('django.conf:settings.dev', namespace='CELERY')
celery.autodiscover_tasks()