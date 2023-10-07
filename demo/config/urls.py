"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from knox import views as knox_views
from products.views import *
from users.views import *
from orders.views import *
from billing.views import *
from cart.views import *
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from products.schema import schema as product_schema
from cart.schema import schema as cart_schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginAPI.as_view()),
    path('register/', Registration_view.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('users/', RetrieveUserView.as_view(), name='retrieve_user'),
    path('users/update/',update_user_view.as_view(),name='update user'),
    path('users/delete/',delete_user.as_view(),name='delete user'),

    path('addresses/create/', CreateAddressView.as_view(), name='create_address'),
    path('addresses/', RetrieveAddressView.as_view(), name='retrieve_address'),
    path('products/graphql',csrf_exempt(GraphQLView.as_view(graphiql=True,schema=product_schema))),
    path('carts/graphql',csrf_exempt(GraphQLView.as_view(graphiql=True,schema=cart_schema))),

    path('products/create/', CreateProductView.as_view(), name='create_product'),
    path('products/<int:pk>/', RetrieveProductView.as_view(), name='retrieve_product'),

    path('carts/create/', CreateCartView.as_view(), name='create_cart'),
    path('carts/', RetrieveCartView.as_view(), name='retrieve_cart'),

    path('product-images/create/', CreateProductImageView.as_view(), name='create_product_image'),
    path('product-images/<int:pk>/', RetrieveProductImageView.as_view(), name='retrieve_product_image'),


    path('orders/<int:pk>/', RetrieveOrderView.as_view(), name='retrieve_order'),
    path('products/search/', ProductSearchView.as_view(), name='product_search'),

    path('orders/', ListOrderView.as_view(), name='order_list'),
    path('order/',order_view.as_view(),name='order_view'),
    path('checkout/',checkout_view.as_view(),name='checkout'),
    path('order_confirm/',order_confirm.as_view(),name='order_confirm'),
    path('invoice/',invoice_genration.as_view(),name='invoice genration'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
   path("reset",reset_confirm.as_view(),name='confirm_reset'),
   path("change_password/",ChangePasswordView.as_view(),name='change_password'),
]
