from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer

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

@api_view(['GET', 'PUT'])
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

@api_view()
def collection_details(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serialize = ProductSerializer(collection)
    return Response(serialize.data)

    