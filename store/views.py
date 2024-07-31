from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from django.db.models import Count
from .models import Product, Collection, OrderItem, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk )
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # def get_serializer_context(self):
    #     return {'product_id': self.kwargs.get('product_pk')}
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


        # Use 'product_pk' to get the nested product context
        # context = super().get_serializer_context()
        # context['product_id'] = self.kwargs.get('product_pk')
        # return context

    # def delete(self, request, pk):
    #     review = get_object_or_404(Collection, pk=pk )
    #     if review.product.count() > 0:
    #         return Response({'error': 'Review cannot be deleted because it is associated with a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     review.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer 

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer

    
    
    
    
    # def get(self, request):
    #     queryset = Product.objects.all()
    #     serialize = ProductSerializer(queryset, many=True, context={'request': request})
    #     return Response(serialize.data)
    
    # def post(self, request):
    #     serialize = ProductSerializer(data=request.data)
    #     serialize.is_valid(raise_exception=True)
    #     serialize.save()
    #     return Response(serialize.data, status=status.HTTP_201_CREATED)
    
# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    # def get(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serialize = ProductSerializer(product)
    #     return Response(serialize.data)
    
    # def put(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serialize = ProductSerializer(product, data=request.data)
    #     serialize.is_valid(raise_exception=True)
    #     serialize.save()


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

    # def get(self, request):
    #     queryset = Collection.objects.annotate(products_count=Count('products'))
    #     serialize = CollectionSerializer(queryset, many=True, context={'request': request})
    #     return Response(serialize.data)
    
    # def post(self, request):
    #     serialize = CollectionSerializer(data=request.data)
    #     serialize.is_valid(raise_exception=True)
    #     serialize.save()
    #     return Response(serialize.data, status=status.HTTP_201_CREATED)
    
# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk )
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it is associated with a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    # def get(self, request, pk):
    #     collection = get_object_or_404(
    #         Collection.objects.annotate(products_count=Count('products')), pk=pk
    #     )
    #     serialize = CollectionSerializer(collection)
    #     return Response(serialize.data)
    
    # def put(self, request, pk):
    #     collection = get_object_or_404(
    #         Collection.objects.annotate(products_count=Count('products')), pk=pk
    #     )
    #     serialize = CollectionSerializer(collection, data=request.data)
    #     serialize.is_valid(raise_exception=True)
    #     serialize.save()
    #     return Response(serialize.data)
    
    

        

    