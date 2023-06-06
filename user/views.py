from rest_framework import generics

from user.models import CustomUser
from user.serializers import CustomUserSerializer


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
