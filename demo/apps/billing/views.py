from rest_framework.generics import *
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
import secrets
from rest_framework.permissions import IsAuthenticated
import json
import requests
from orders.models import *
from users.utils import order_invoice_genration_mail
from .tasks import check_order
# Create your views here.



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
                                product_order_list.append(product_order(order=Order,product=i,quantity=j['quantity'],price=j['quantity']*i.price_per_unit))
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


class invoice_genration(APIView):
    def post(self,request):
        try:
            if request.user is None:
                raise ValueError("invalid user")
            user=request.user
            Order=request.data['order']
            Order=order.objects.get(order_id=Order)
            email_factory = order_invoice_genration_mail.from_request(
                self.request, user=user
            )

            email_factory.get_order(Order)
            email = email_factory.create()
            print(email.__dict__)
            output=email.send()
            return Response({'success':'invoice sent'},status=200)
        except Exception as e:
            return Response({'error':str(e)},status=400)
