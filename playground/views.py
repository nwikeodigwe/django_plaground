import logging
from django.shortcuts import render
from rest_framework.views import APIView
# from django.utils.decorators import method_decorator
# from django.core.cache import cache
# from django.views.decorators.cache import cache_page
import requests
# from .tasks import notify_customers
# from django.core.mail import EmailMessage, BadHeaderError
# from templated_mail.mail import BaseEmailMessage
# from django.core.mail import send_mail, mail_admins, BadHeaderError
# from django.contrib.contenttypes.models import ContentType
# from store.models import Product

logger = logging.getLogger(__name__)

class HelloView(APIView):
    # @method_decorator(cache_page(5 * 60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Received the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')

        return render(request, 'hello.html', {"name": data})


# Create your views here.
# A view function is a function that takes a request and returns a response
# @cache_page(5 * 60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
    # key = 'httpbin_result'
    # if cache.get(key) is None:
    #     response = requests.get('https://httpbin.org/delay/2')
    #     data = response.json()
    #     cache.set(key, data)
    # notify_customers.delay('Hello')
    # try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Nwike'}
    #     )
    #     message.send(['joe@email.com'])
        # message = EmailMessage('subject', 'message', 'from@email.com', ['joe@email.com'])
        # message.attach_file('playground/static/images/image.jpg')
        # message.send()
        # send_mail('subject', 'message', 'info@moshbuy.com', ['bob@moshby.com'])
        # mail_admins('subject', 'message', html_message='message')
    # except BadHeaderError:
    #     pass
    # return render(request, 'hello.html', {"name": data})
