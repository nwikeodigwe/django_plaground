release: Python manage.py migrate
web: gunicorn ecommerce.wsgi
worker: celery -A ecommerce worker