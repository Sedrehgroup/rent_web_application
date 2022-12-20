from django.urls import path
from .views import (
    ListCreateContract,
    RetrieveUpdateDestroyContract,
    LeaseAPIView,
    ContractCompleteAPIView
)

urlpatterns = [
    path('list_create_contract/', ListCreateContract().as_view()),
    path('modify_contract/<int:pk>/', RetrieveUpdateDestroyContract().as_view()),
    path("lease/<int:pk>/", LeaseAPIView.as_view(), name="lease"),
    path("complete-contract/", ContractCompleteAPIView.as_view(), name="complete-contract"),
]
