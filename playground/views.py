from django.http import HttpResponse
# from django.shortcuts import render

# Create your views here.
# A view function is a function that takes a request and returns a response

def say_hello(request):
    return HttpResponse('Hello World!')
