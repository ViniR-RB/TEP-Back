from django.urls import path

from api.views import StockView

urlpatterns = [
    path('stock/', StockView.as_view(), name='stock'),
]
