from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.filters import SearchFilter
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
import secrets
from rest_framework.permissions import IsAuthenticated,AllowAny
import json
import requests
from django.urls import reverse

# Create your views here.


class CreateCartView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = cart.objects.all()
    serializer_class = CartSerializer

class RetrieveCartView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    def get_queryset(self):
        return cart.objects.filter(user=self.request.user)
