from rest_framework import generics
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from user.models import CustomUser
from user.serializers import (CustomTokenObtainPairSerializer,
                              CustomUserSerializer)


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    pass
