from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
# from pprint import pprint

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(product_router.urls)),
# ]

# URLConf
urlpatterns = router.urls + product_router.urls
# urlpatterns = [
#     path('', include(router.urls)),
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetails.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetails.as_view(), name='collection-details')
# ]