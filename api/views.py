from django.db.models import DecimalField, F, Sum
from django.db.models.expressions import RawSQL
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import *
from user.serializers import *
from user.serializers import CustomUser, Investor


class StockView(APIView):
    def get(self, request, stock_id=None):
        if stock_id is not None:
            stock = self.get_object(stock_id)
            if stock:
                serializer = StockSerializer(stock)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data={"msg": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, stock_id):
        try:
            return Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            return None

    def put(self, request, stock_id):
        stock = self.get_object(stock_id)
        if stock:
            serializer = StockSerializer(stock, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Stock not found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, stock_id):
        stock = self.get_object(stock_id)
        if stock:
            stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Stock not found", status=status.HTTP_404_NOT_FOUND)


class TransactionView(APIView):
    def get(self, request, transaction_id=None):
        if transaction_id is not None:
            transaction = self.get_object(transaction_id)
            if transaction:

                serializer = TransactionSerializer(transaction)
                price_total = transaction.calculate_price_total()
                total_value = transaction.calculate_total_value()
                data = {"transaction": serializer.data,
                        "price_total": price_total, "total_value": total_value}
                return Response(data, status=status.HTTP_200_OK)
            return Response(data={"msg": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        transaction = Transaction.objects.all()
        transaction = transaction.annotate(
            price_total=F('price_unit') * F('quantity'))
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self, transaction_id):
        try:
            return Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return None

    def delete(self, request, transaction_id):
        transaction = self.get_object(transaction_id)
        if transaction:
            stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Transaction not Found", status=status.HTTP_404_NOT_FOUND)


class TransactionFromInvestorView(APIView):
    def get(self, request, investor_id=None):
        investor_id = request.user.id
        transactions = Transaction.objects.all()
        if investor_id:
            transactions = Transaction.objects.filter(investor=investor_id)
        compra = transactions.filter(operation='C')
        venda = transactions.filter(operation='V')

        profit = sum(transaction.calculate_total_value()
                     for transaction in compra)
        prejuizo = sum(transaction.calculate_total_value()
                       for transaction in venda)
        profit_total = profit - prejuizo
        valor_total = sum(transaction.calculate_total_value()
                          for transaction in transactions)
        serializer = TransactionSerializer(
            transactions, many=True, context={'request': request})
        data = {'transactions': serializer.data,
                'valor_total': valor_total,
                'profit': profit,
                'prejuizo': prejuizo,
                'profit_total': profit_total
                }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, transaction_id):

        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({'msg': 'Transação não encontrada.'}, status=404)

        serializer = TransactionSerializer(
            transaction, data=request.data, partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, transaction_id):
        transaction = self.get_object(transaction_id, request.user.id)
        if transaction:
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={'msg': 'Transaction not Found'}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self, transaction_id, investor_id):
        try:
            return Transaction.objects.get(investor=investor_id, id=transaction_id)
        except Transaction.DoesNotExist:
            return None


class InvestorView(APIView):

    def get(self, request, user_id=None):
        if user_id is not None:
            investor = self.get_object(user_id)
            if investor:
                serializer = InvestorSerializer(investor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data={"msg": "Investor not found"}, status=status.HTTP_404_NOT_FOUND)
        investor = Investor.objects.all()
        serializer = InvestorSerializer(investor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        try:
            investor = Investor.objects.get(user=user_id)
        except Investor.DoesNotExist:
            return Response({"message": "Investidor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvestorSerializer(
            investor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, user_id):
        try:
            return Investor.objects.get(user=user_id)
        except Investor.DoesNotExist:
            return None


class ProfitGlobalView(APIView):
    def get(self, request):
        # Retrieve all transactions
        investor = request.user.id
        transactions = Transaction.objects.filter(investor=investor)
        compra = transactions.filter(operation='C')
        venda = transactions.filter(operation='V')
        profit = sum(transaction.calculate_total_value()
                     for transaction in compra)
        prejuizo = sum(transaction.calculate_total_value()
                       for transaction in venda)
        profit_total = profit - prejuizo

        return Response({'profit_total': profit_total})


class TransactionsByMonthYearView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        transactions = Transaction.objects.filter(

            created_at__year=year,
            created_at__month=month,
        )
        transactions = transactions.filter(investor=request.user.id)

        serialized_transactions = []  # Lista para armazenar as transações serializadas

        # Serializar as transações
        for transaction in transactions:
            serialized_transaction = {
                'stock': transaction.stock.id,
                'quantity': transaction.quantity,
                'investor': transaction.investor.id,
                'brokerage': str(transaction.brokerage),
                'price_unit': str(transaction.price_unit),
                'created_at': transaction.created_at,
                'operation': transaction.operation,
                'tax_b3': str(transaction.tax_b3),
            }
            serialized_transactions.append(serialized_transaction)

        return Response(serialized_transactions)
