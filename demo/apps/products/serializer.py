from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from products import constants

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                        None,
                                        validated_data['password'])
        return user





class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")



class ResetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})
    new_password = serializers.CharField(style={"input_type": "password"})
    re_new_password = serializers.CharField(style={"input_type": "password"})



    def check_user_current_password(self, request,value):

        if not request.user.check_password(value):
            raise serializers.ValidationError(self.error_messages["invalid_password"])
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["re_new_password"]:
            raise serializers.ValidationError(self.error_messages["password_mismatch"])
        return attrs




class UserSerializer(serializers.ModelSerializer):
    """retrieve details of the user"""
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','authorization']


class UserUpdateserializer(serializers.ModelSerializer):
    """to update first name last name and authorization of the user of ther user"""

    class Meta:
        model = User
        fields=['first_name','last_name','authorization']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = adress
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_image
        fields = '__all__'




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        exclude =['secret_key']

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_order
        fields = '__all__'
