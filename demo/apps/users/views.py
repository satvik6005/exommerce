from django.shortcuts import render
from rest_framework.generics import *
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from knox.models import AuthToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from .utils import *


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


class ChangePasswordView(APIView):
    """
    Use this endpoint to change user password.
    """

    permission_classes = (IsAuthenticated,)


    def post(self, request):
        serializer= serializers.ResetPasswordSerializer
        serializer.validate_data(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)






class RetrieveUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer_class = UserSerializer
        user=request.user
        if request.user is not None:
            return Response(serializer_class(user).data,status=200)
        return Response({'error':"user does't exist"},status=404)
# Create your views here.


class ChangePasswordView(APIView):
    """
    Use this endpoint to change user password.
    """

    permission_classes = (IsAuthenticated,)


    def post(self, request):
        try:
            serializer= ResetPasswordSerializer(data=request.data)
            if serializer.is_valid() and serializer.check_user_current_password(request,serializer.data['current_password']):
                self.request.user.set_password(serializer.data["new_password"])
                self.request.user.save()
            return Response({"success":"passwor changed"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error":str(e)},status=400)


class reset_confirm(APIView):

    template_name = "forgot_password.html"


    permission_classes = (AllowAny,)


    def get(self, request, *args, **kwargs):
            return render(
            request,
            self.template_name,
            {"token": request.GET.get('token')},
        )



class CreateAddressView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = adress.objects.all()
    serializer_class = AddressSerializer

class RetrieveAddressView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return adress.objects.filter(user=self.request.user)
