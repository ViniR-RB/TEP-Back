from django.urls import path

from user.views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register-user'),
]
