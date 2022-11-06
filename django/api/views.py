from django.shortcuts import render
from rest_framework import generics
from .models import Rent
from .serializer import RentSerializer


class RentList(generics.ListCreateAPIView):
    serializer_class = RentSerializer

    def get_queryset(self):
        queryset = Rent.objects.all()
        landlord = self.request.query_params.get('landlord')
        tenant = self.request.query_params.get('tenant')
        if landlord is not None:
            queryset = queryset.filter(landlord=landlord)
        if tenant is not None:
            queryset = queryset.filter(tenant=tenant)
        return queryset


class RentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RentSerializer
    queryset = Rent.objects.all()
