from rest_framework import serializers
from .models import *




class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'
