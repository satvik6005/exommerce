from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.filters import SearchFilter
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
import secrets
from .tasks import check_order
from knox.models import AuthToken
from rest_framework.permissions import IsAuthenticated
import json

# Create your views here.




class Registration_view(GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_class=[]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "id":user.id,   
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        },status=201)


class LoginAPI(GenericAPIView):
    serializer_class = LoginUserSerializer
    permssion_class=[]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "id":user.id,
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class update_user_view(UpdateAPIView):
    serializer_class = UserUpdateserializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the user profile of the currently authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=200)

    


class delete_user(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request):
   
        user=request.user
        print(user)
        if user is not None:
            user.delete()
            return Response({"success":"user deleted successfully"},status=200)
        return Response({'error':"user does't exist"},status=404)

class RetrieveUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer_class = UserSerializer
        user=request.user
        if request.user is not None:
            return Response(serializer_class(user).data,status=200)
        return Response({'error':"user does't exist"},status=404)
    


class CreateAddressView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = adress.objects.all()
    serializer_class = AddressSerializer

class RetrieveAddressView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return adress.objects.filter(user=self.request.user)

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

class CreateCartView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = cart.objects.all()
    serializer_class = CartSerializer

class RetrieveCartView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    def get_queryset(self):
        return cart.objects.filter(user=self.request.user)
    
    

class CreateProductImageView(CreateAPIView):
    queryset = Product_image.objects.all()
    serializer_class = ProductImageSerializer

class RetrieveProductImageView(RetrieveAPIView):
    queryset = Product_image.objects.all()
    serializer_class = ProductImageSerializer


class RetrieveOrderView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = order.objects.all()
    serializer_class = OrderSerializer
  
class ListOrderView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get_queryset(self):
        return order.objects.filter(user=self.request.user)



class order_view(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            user=request.user
            print(user)
            print(request.data.get('cart'))
            if request.data.get('cart')==True:
                print("running")
                products=cart.cart_product(user)
                products_to_buy=list(cart.cart_objects(user).values('product','quantity'))
                print(products,products_to_buy)
            elif request.data.get('cart')==False:
                products=Product.objects.filter(id=request.data.get('product'))
                products_to_buy=[dict({'product':request.data.get('product'),'quantity':request.data.get('quantity')})]
            print(products,products_to_buy)
            final_price=0
            for i in products:
                for j in products_to_buy:
                    if i.id==j["product"]:
                        if i.available_units<j["quantity"]:

                            raise ValueError('not enough quantity')
                        else:
                            j['price']=j['quantity']*i.price_per_unit
                            final_price+=j['price']

            response=dict()
            
            # Order=OrderSerializer(user=user,del_adress=adress.objects.get(id=request.data.get('del_adress')),final_price=final_price)

            # print(f"products decremented and final price calculated {final_price}")
            # response['order']=Order.data
            response['products']=products_to_buy

            response['final_price']=final_price
            response['del_adress']=request.data['del_adress']
            

            return Response(response,status=200)
            
            
            
            
                
            
        
        except Exception as e:
                    return Response({'error':str(e)},status=400)





class checkout_view(APIView):
            permission_class = [IsAuthenticated]
            def post(self,request):
                try:
                    user=request.user
                    products_to_buy=request.data['products']
                    
                    products=Product.get_products([i['product'] for i in products_to_buy])
                    
                    print(products,products_to_buy)
                    final_price=0
                    for i in products:
                        for j in products_to_buy:
                            if i.id==j["product"]:
                                print(i)
                                if i.available_units<j["quantity"]:

                                    raise ValueError('not enough quantity')
                                else:
                                    j['price']=j['quantity']*i.price_per_unit
                                    final_price+=j['price']
                    if request.data['final_price']!=final_price:
                        raise ValueError('price changed order again')
                    Order=order.objects.create(user=user,del_adress=adress.objects.get(id=request.data['del_adress']),final_price=final_price,secret_key=secrets.token_urlsafe(20))
                    print(order)
                    print('running')
                    product_order_list=[]
                    for i in products:
                        for j in products_to_buy:
                            if i.id==j['product']:
                                product_order_list.append(product_order(order=Order,product=i,quantity=j['quantity']))
                    print(product_order_list)
                    product_order.objects.bulk_create(product_order_list)
                    print("runing")
                    print(check_order.apply_async((Order.order_id,),countdown=240,expires=245))
                    return Response({"url":f"http://127.0.0.1:8000/order_confirm?order={Order.order_id}&token={Order.secret_key}"},status=200)

                    
                    
                except Exception as e:
                    return Response({'error':str(e)},status=400)


class order_confirm(APIView):
    def get(self,request,format=None):
        try:
            order_id=request.query_params.get('order')
            secret=request.query_params.get('token')
            Order=order.objects.get(order_id=order_id)
            if Order.order_placed==1:
                return ValueError('invalid order')
            if Order.expired==1:
                return Response({'error':'order expired place again'},status=400)
            if Order.secret_key==secret:
                Order.order_placed=1
                Order.expired=1
                Order.save()
                return Response({'success':'order created'},status=201)
            else:
                return Response({'error':'order not placed'},status=400)
        except Exception as e:
            return Response({'error':str(e)},status=400)
        










    

