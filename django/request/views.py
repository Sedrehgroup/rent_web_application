from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from .models import Request
from request.permissions import IsNotOwner
from .serializer import RequestSerializer, CreateRequestSerializer, LandlordUpdateRequestSerializer
from rest_framework.permissions import IsAuthenticated


class CreateListRequests(ListCreateAPIView):
    serializer_class = RequestSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            # Create
            self.permission_classes = [IsAuthenticated, IsNotOwner]
        else:
            # List
            self.permission_classes = [IsAuthenticated]
        return super(CreateListRequests, self).get_permissions()

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


class LandlordUpdateRequest(UpdateAPIView):
    serializer_class = LandlordUpdateRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Request.objects.filter(request_property__owner=self.request.user).select_related("request_property")
        return queryset

