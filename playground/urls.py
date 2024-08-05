from django.urls import path

from . import views

#This is a URLConf module basically meaning URL configuration
urlpatterns = [
    path('hello/', views.HelloView.as_view())
]