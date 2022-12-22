from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from .models import Contract
from contract.permissions import IsLandlord, ObjectIsLandlord, ObjectIsTenant, IsUserCompletePermission
from .serializer import ContractSerializer, LeaseSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ListCreateContract(ListCreateAPIView):
    serializer_class = LeaseSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            # Create
            self.permission_classes = [IsAuthenticated, IsLandlord, IsUserCompletePermission]
        else:
            # List
            self.permission_classes = [IsAuthenticated, IsUserCompletePermission]
        return super(ListCreateContract, self).get_permissions()

    def get_queryset(self):
        queryset = Contract.objects.filter(
            Q(contract_tenant=self.request.user) | Q(contract_landlord=self.request.user),
            document_status__in=[0,1,2,4,6]
            )
        return queryset


class RetrieveUpdateDestroyContract(RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ObjectIsLandlord | ObjectIsTenant, IsUserCompletePermission]
    
    def get_queryset(self):
        queryset = Contract.objects.exclude(document_status=3)
        return queryset


class LeaseAPIView(RetrieveAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contract.objects.filter(Q(contract_tenant=self.request.user) | Q(contract_landlord=self.request.user))
        return queryset


class LeasedCompleteAPIView(ListAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contract.objects.filter(
            contract_landlord=self.request.user,
            document_status=3
            )
        return queryset


class RentedCompleteAPIView(ListAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contract.objects.filter(
            contract_tenant=self.request.user,
            document_status=3
            )
        return queryset


class ContractCounter(APIView):
    permission_classes = [IsAuthenticated]

    def get_num_leased(self):
        leased = Contract.objects.filter(contract_landlord=self.request.user, document_status=3)
        return leased.count()

    def get_num_rented(self):
        rented = Contract.objects.filter(
            contract_tenant=self.request.user, document_status=3)
        return rented.count()

    def get_num_incomplete(self):
        incomplete = Contract.objects.filter(
            Q(contract_tenant=self.request.user) | Q(contract_landlord=self.request.user),
            document_status__in=[0,1,2,4,6]
            )
        return incomplete.count()

    def get(self, request):
        data = {
            "number_leased": self.get_num_leased(),
            "number_rented": self.get_num_rented(),
            "number_incomplete": self.get_num_incomplete()
        }
        return Response(data, status=status.HTTP_200_OK)
