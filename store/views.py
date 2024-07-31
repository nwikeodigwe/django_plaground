from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count
from .models import Product, Collection
from .serializers import CollectionSerializer, ProductSerializer

class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serialize = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serialize.data)
    
    def post(self, request):
        serialize = ProductSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data, status=status.HTTP_201_CREATED)
    
class ProductDetails(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serialize = ProductSerializer(product)
        return Response(serialize.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serialize = ProductSerializer(product, data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()

    def delete(self, request):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serialize = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serialize.data)
    
    def post(self, request):
        serialize = CollectionSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data, status=status.HTTP_201_CREATED)
    
class CollectionDetails(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')), pk=pk
        )
        serialize = CollectionSerializer(collection)
        return Response(serialize.data)
    
    def put(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')), pk=pk
        )
        serialize = CollectionSerializer(collection, data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data)
    
    def delete(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')), pk=pk
        )
        if collection.product.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        

    