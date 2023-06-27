from django.urls import path

from api.views import (InvestorView, ProfitGlobalView, StockView,
                       TransactionFromInvestorView,
                       TransactionsByMonthYearView, TransactionView)

urlpatterns = [
    path('stock/', StockView.as_view(), name='stock'),
    path('stock/<int:stock_id>/', StockView.as_view(), name='stock-update-delete'),
    path('my/transaction/', TransactionFromInvestorView.as_view(), name='my-transaction'),
    path('my/transaction/<int:transaction_id>/', TransactionFromInvestorView.as_view(), name='my-transaction'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('transaction/<int:transaction_id>/', TransactionView.as_view(), name='transaction'),
    path('transaction/<str:name_code_stock>/', TransactionView.as_view(), name='transaction'),
    path('investor/', InvestorView.as_view(), name='investor'),
    path('investor/<int:user_id>/', InvestorView.as_view(), name='investor'),
    path('my/profit/', ProfitGlobalView.as_view(), name='profit'),
    path('transactions/<int:year>/<int:month>/', TransactionsByMonthYearView.as_view(), name='transactions-by-month-year'),
]
