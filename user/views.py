from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.serializers import *
from user.models import CustomUser
from user.serializers import (CustomTokenObtainPairSerializer,
                              CustomUserSerializer, InvestorSerializer)


# Create your views here.
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            print(user)
            investor_data = { "user": user.id,'profile_risk': 'moderado'}
            investor_serializer = InvestorSerializer(data=investor_data)
            print(investor_serializer.is_valid(raise_exception=True))
            if investor_serializer.is_valid():
                investor_serializer.save()
                return Response({'msg': 'Usuário e o seu Perfil Foram Criados'})
            else:
                user.delete()
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    pass
