from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .models import CustomerProfile , Order
from .serializers import CustomerProfileSerializer , OrderSerializer


class CustomerProfileView(APIView):
    def profile(self , request):
        serializer =CustomerProfileSerializer(data=request.data) #deserialize the incoming json data


        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_Created)
        
        return Response(status=status.HTTP_400_BAD_Created)


class OrderView(APIView):
    def Order(self , request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_Created)
        
        return Response(status=status.HTTP_400_BAD_Created)
    



