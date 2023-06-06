from django.urls import path

from user.views import (CustomTokenObtainPairView, CustomTokenRefreshView,
                        UserRegistrationView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register-user'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
