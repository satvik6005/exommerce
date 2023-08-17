from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.filters import SearchFilter
from .serializer import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
import secrets
from .tasks import check_order
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


class order_view(APIView):
    def post(self,request):
        try:
            user=User.objects.get(pk=request.data.get('user'))
            print(user)
            print(request.data.get('cart'))
            if request.data.get('cart')==1 and request.data.get('direct')==1:
                raise ValueError('both cart and direct cannot be true')
            
            if request.data.get('cart')==1:
                print("running")
                products=cart.cart_product(user)
                products_to_buy=list(cart.cart_objects(user).values('product','quantity'))
                print(products,products_to_buy)
            elif request.data.get('direct')==1:
                products=Product.objects.filter(id=request.data.get('product'))
                products_to_buy=[dict({'product':request.data.get('product'),'quantity':request.data.get('quantity')})]
            print(products,products_to_buy)
            for i in products:
                for j in products_to_buy:
                    if i.id==j["product"]:
                        if i.available_units<j["quantity"]:
                            raise ValueError('not enough quantity')
            final_price=0
            product_order_list=[]
            Order=order.objects.create(user=user,del_adress=adress.objects.get(id=request.data.get('del_adress')),final_price=final_price,secret_key=secrets.token_urlsafe(20))
            for i in products:
                for j in products_to_buy:
                    if i.id==j["product"]:
                        Product.objects.filter(id=i.id).update(available_units=F('available_units')-j["quantity"])
                        final_price+=i.price_per_unit*j['quantity']
                        product_order_list.append(product_order(order=Order,product=i,quantity=j['quantity']))
            print(f"products decremented adn inal price calculated {final_price}")
            
            
            
            
                
            product_order.objects.bulk_create(product_order_list)
            print(check_order.apply_async((Order.order_id,),countdown=5,expires=10))

                

            
            
            
            

            
            
            
            return Response({"url":f"http://127.0.0.1:8000/order_confirm?order={Order.order_id}&token={Order.secret_key}"},status=200)

            
            
        except Exception as e:
            return Response({'error':str(e)},status=400)


class order_confirm(APIView):
    def get(self,request,format=None):
        try:
            order_id=request.query_params.get('order')
            secret=request.query_params.get('token')
            Order=order.objects.get(order_id=order_id)
            if Order.expired==1:
                return Response({'error':'order expired place again'},status=400)
            if Order.secret_key==secret:
                Order.order_placed=1
                Order.save()
                return Response({'success':'order created'},status=201)
            else:
                return Response({'error':'order not placed'},status=400)
        except Exception as e:
            return Response({'error':str(e)},status=400)
        










    

