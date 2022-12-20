from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, \
    CreateAPIView
from .models import Property
from .serializer import PropertySerializer
from rest_framework.permissions import IsAuthenticated
from property.pagination import PropertyPagination
from rest_framework.parsers import MultiPartParser


class PropertyList(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PropertyPagination
    filterset_fields = ['county', 'city']
    queryset = Property.objects.filter(is_public=False).order_by("-created_date")

class ListMyProperties(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PropertyPagination
    filterset_fields = ['county', 'city']

    def get_queryset(self):
        queryset = Property.objects.filter(owner=self.request.user).order_by("-created_date")
        return queryset


class CreateMyProperties(CreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['county', 'city']
    pagination_class = PropertyPagination
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        queryset = Property.objects.filter(owner=self.request.user).order_by("-created_date")
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrieveUpdateDestroyProperties(RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        queryset = Property.objects.filter(owner=self.request.user)
        return queryset


class RetrieveProperties(RetrieveAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Property.objects.filter(is_public=True).order_by("-created_date")
        return qs
