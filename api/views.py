from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import *


class StockView(APIView):
    def get_object(self, pk):
        try:
            return Stock.objects.get(pk=pk)

        except:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        stock = self.get_object(pk)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stock = self.get_object(pk)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
