from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from .models import Contract
from contract.permissions import IsTenant, IsLandlord, ObjectIsLandlord, ObjectIsTenant
from .serializer import ContractSerializer, LeaseSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class ListCreateContract(ListCreateAPIView):
    serializer_class = ContractSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            # Create
            self.permission_classes = [IsAuthenticated, IsLandlord | IsTenant]
        else:
            # List
            self.permission_classes = [IsAuthenticated]
        return super(ListCreateContract, self).get_permissions()

    def get_queryset(self):
        queryset = Contract.objects.filter(
            Q(contract_tenant=self.request.user) | Q(contract_landlord=self.request.user),
            document_status__in=[0,1,2,4,6]
            )
        return queryset


class RetrieveUpdateDestroyContract(RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ObjectIsLandlord | ObjectIsTenant]
    
    def get_queryset(self):
        queryset = Contract.objects.exclude(document_status=3)
        return queryset


class LeaseAPIView(RetrieveAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contract.objects.filter(Q(contract_tenant=self.request.user) | Q(contract_landlord=self.request.user))
        return queryset


class ContractCompleteAPIView(ListAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Contract.objects.filter(
            Q(contract_tenant=self.request.user) | Q(contract_landlord=self.request.user),
            document_status=3
            )
        return queryset
