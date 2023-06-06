from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import *


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
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer =  TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
