from rest_framework import serializers
from .models import *




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        exclude =['secret_key']

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_order
        fields = '__all__'
