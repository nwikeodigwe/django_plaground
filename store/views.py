from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, F
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission

# from core import serializers
from .filters import ProductFilter
from .pagination import DefaultPagination
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from .models import CartItem, Customer, Order, Product, Collection, OrderItem, ProductImage, Review, Cart
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, UpdateOrderSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    # filterset_fields = ['collection_id', 'unit_price']
    # pagination_class = PageNumberPagination
    # pagination_class = LimitOffsetPagination
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id', None)
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

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
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk )
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    # queryset = Cart.objects.prefetch_related('items__product').all()
    queryset = Cart.objects.prefetch_related('items__product').annotate(total_price=Sum(F('items__quantity') * F('items__product__unit_price')))
    serializer_class = CartSerializer  
    

class CartItemViewSet(ModelViewSet):
    http_method_names =  ['get', 'post', 'patch', 'delete']
    # queryset = CartItem.objects.all()
    # serializer_class = CartItemSerializer 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [fullDjangoModelPermissions]
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serialize = CustomerSerializer(customer)
            return Response(serialize.data)
        elif request.method == 'PUT':
            serialize = CustomerSerializer(customer, data=request.data)
            serialize.is_valid(raise_exception=True)
            serialize.save()
            return Response(serialize.data)
    
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')
    
class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post', 'patch', 'delete', 'head', 'options']
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        
        (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
    
    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    # queryset = ProductImage.objects.all()

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

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
    
    

        

    