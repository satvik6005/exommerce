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
from django.urls import path,include
from knox import views as knox_views
from products.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginAPI.as_view()),
    path('register/', Registration_view.as_view()),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/', include('knox.urls')),
    path('users/<int:pk>/', RetrieveUserView.as_view(), name='retrieve_user'),
    path('users/update/<int:pk>/',update_user_view.as_view(),name='update user'),

    path('addresses/create/', CreateAddressView.as_view(), name='create_address'),
    path('addresses/<int:pk>/', RetrieveAddressView.as_view(), name='retrieve_address'),

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
    path('order_confirm/',order_confirm.as_view(),name='order_confirm')
]
