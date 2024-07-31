from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_details),
    path('collections/', views.collection_list),
    path('collections/<int:pk>/', views.collection_details, name='collection-details')
]