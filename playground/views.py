from django.shortcuts import render
# from django.contrib.contenttypes.models import ContentType
# from store.models import Product


# Create your views here.
# A view function is a function that takes a request and returns a response

def say_hello(request):
    return render(request, 'hello.html', {"name": "Nwike"})
