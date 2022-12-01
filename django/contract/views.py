from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Contract
from permissions import IsTenant, IsLandlord, ObjectIsLandlord, ObjectIsTenant
from .serializer import ContractSerializer
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
        queryset = Contract.objects.filter(Q(contract_tenant=self.request.user) | Q(contract_landlord=self.request.user))
        return queryset


class RetrieveUpdateDestroyContract(RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ObjectIsLandlord | ObjectIsTenant]
    queryset = Contract.objects.all()
