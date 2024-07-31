from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Product, Collection
from .serializers import CollectionSerializer, ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.all()
        serialize = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serialize.data)
    elif request.method == 'POST':
        serialize = ProductSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serialize = ProductSerializer(product)
        return Response(serialize.data)
    elif request.method == 'PUT':
        serialize = ProductSerializer(product, data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data)
    elif request.method == 'DELETE':
        if product.orderitem.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serialize = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serialize.data)
    elif request.method == 'POST':
        serialize = CollectionSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_details(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count('products')), pk=pk
    )
    if request.method == 'GET':
        serialize = CollectionSerializer(collection)
        return Response(serialize.data)
    elif request.method == 'PUT':
        serialize = CollectionSerializer(collection, data=request.data)
        serialize.is_valid(raise_exception=True)
        serialize.save()
        return Response(serialize.data)
    elif request.method == 'DELETE':
        if collection.product.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    