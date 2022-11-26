from rest_framework.generics import ListAPIView, ListCreateAPIView
from .models import Property
from .serializer import PropertySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


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


