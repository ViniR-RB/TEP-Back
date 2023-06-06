from django.urls import path

from api.views import StockView, TransactionView

urlpatterns = [
    path('stock/', StockView.as_view(), name='stock'),
    path('stock/<int:stock_id>/', StockView.as_view(), name='stock-update-delete'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
]
