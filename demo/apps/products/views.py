from rest_framework.generics import *
from rest_framework.filters import SearchFilter
from .serializer import *
from .models import *
from rest_framework.permissions import IsAuthenticated




class CreateProductView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class RetrieveProductView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name','desc']




class CreateProductImageView(CreateAPIView):
    queryset = Product_image.objects.all()
    serializer_class = ProductImageSerializer

class RetrieveProductImageView(RetrieveAPIView):
    queryset = Product_image.objects.all()
    serializer_class = ProductImageSerializer
