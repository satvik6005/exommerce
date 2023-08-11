from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.filters import SearchFilter
from .serializer import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RetrieveUserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateAddressView(CreateAPIView):
    queryset = adress.objects.all()
    serializer_class = AddressSerializer

class RetrieveAddressView(RetrieveAPIView):
    queryset = adress.objects.all()
    serializer_class = AddressSerializer

class CreateProductView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RetrieveProductView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name'] 

class CreateCartView(CreateAPIView):
    queryset = cart.objects.all()
    serializer_class = CartSerializer

class RetrieveCartView(ListAPIView):
    queryset = cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

class CreateProductImageView(CreateAPIView):
    queryset = Product_image.objects.all()
    serializer_class = ProductImageSerializer

class RetrieveProductImageView(RetrieveAPIView):
    queryset = Product_image.objects.all()
    serializer_class = ProductImageSerializer


class RetrieveOrderView(RetrieveAPIView):
    queryset = order.objects.all()
    serializer_class = OrderSerializer
  
class ListOrderView(ListAPIView):
    queryset = order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']








    

