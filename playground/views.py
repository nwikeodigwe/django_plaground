from django.shortcuts import render
from .tasks import notify_customers
# from django.core.mail import EmailMessage, BadHeaderError
# from templated_mail.mail import BaseEmailMessage
# from django.core.mail import send_mail, mail_admins, BadHeaderError
# from django.contrib.contenttypes.models import ContentType
# from store.models import Product


# Create your views here.
# A view function is a function that takes a request and returns a response

def say_hello(request):
    notify_customers.delay('Hello')
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
    return render(request, 'hello.html', {"name": "Nwike"})
