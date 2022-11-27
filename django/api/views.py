from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import Property, Request, Contract
from .permissions import IsTenant, IsLandlord
from .serializer import PropertySerializer, ContractSerializer, RequestSerializer, CreateRequestSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q


class PropertyList(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    queryset = Property.objects.all()


class CreateListMyProperties(ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Property.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=[self.request.user])


class RetrieveUpdateDestroyProperties(RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Property.objects.filter(owner=self.request.user)
        return queryset


class CreateListRequests(ListCreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateRequestSerializer
        return RequestSerializer

    def get_queryset(self):
        queryset = Request.objects.filter(tenant=self.request.user).select_related("request_property")
        return queryset

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)


class ListRequestsToMe(ListAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Request.objects.filter(request_property__owner=self.request.user).select_related("request_property")
        return queryset


class RetrieveUpdateDestroyRequests(RetrieveUpdateDestroyAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Request.objects.filter(tenant=self.request.user)
        return queryset


class ListCreateContract(ListCreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contract.objects.all()


class RetrieveUpdateDestroyContract(RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsLandlord | IsTenant]
    queryset = Contract.objects.all()



