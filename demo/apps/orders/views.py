from django.shortcuts import render
from rest_framework.generics import *
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from rest_framework.permissions import IsAuthenticated
import json
import requests
from django.urls import reverse
from cart.models import cart
from products.models import Product

# Create your views here.



class RetrieveOrderView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = order.objects.all()
    serializer_class = OrderSerializer

class ListOrderView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get_queryset(self):
        return order.objects.filter(user=self.request.user)



    def post(self, request, *args, **kwargs):
        post_data = {
            "token": request.GET["token"],
            "new_password": request.POST["new_password"],
            "re_new_password": request.POST["re_new_password"],
        }

        errors = []
        success=False
        if post_data['new_password']!=post_data['re_new_password']:
            errors.append('password doestt match')
        else:

            baseurl = request.build_absolute_uri(reverse("password_reset:reset-password-confirm"))
            headers = {'Content-type': 'application/json'}

            data={"token":post_data['token'],"password":post_data['new_password']}
            result = requests.post(baseurl, data=json.dumps(data),headers=headers)

            if result.status_code == 200:
                success = True
            else:
                result_dict = result.json()
                for key, val in result_dict.items():
                    errors.append(key + " : ".join(val))
        return render(
            request, self.template_name, {"success": success, "errors": errors}
        )



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
            if not adress.objects.filter(id=request.data['del_adress']).exists() :
                raise ValueError("invalid adress")
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
