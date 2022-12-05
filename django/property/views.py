from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Property
from .serializer import PropertySerializer
from rest_framework.permissions import IsAuthenticated
from property.pagination import PropertyPagination


class PropertyList(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PropertyPagination
    filterset_fields = ['county', 'city']
    queryset = Property.objects.all().order_by("-created_date")


class CreateListMyProperties(ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PropertyPagination

    def get_queryset(self):
        queryset = Property.objects.filter(owner=self.request.user).order_by("-created_date")
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrieveUpdateDestroyProperties(RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Property.objects.filter(owner=self.request.user)
        return queryset

