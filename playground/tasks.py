from time import sleep
# from ecommerce.celery import celery
from celery import shared_task

# @celery.task
@shared_task
def notify_customers(message):
    print('Sending 10K emails...')
    sleep(10)
    print(message)
    print('Emails were successfully sent!')