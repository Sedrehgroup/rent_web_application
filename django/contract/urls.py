from django.urls import path
from .views import (
    ListCreateContract,
    RetrieveUpdateDestroyContract,
    LeaseAPIView,
    LeasedCompleteAPIView,
    RentedCompleteAPIView,
    ContractCounter
)

urlpatterns = [
    path('list_create_contract/', ListCreateContract().as_view()),
    path('modify_contract/<int:pk>/', RetrieveUpdateDestroyContract().as_view()),
    path("lease/<int:pk>/", LeaseAPIView.as_view(), name="lease"),
    path("complete-leased/", LeasedCompleteAPIView.as_view(), name="complete-leased"),
    path("complete-rented/", RentedCompleteAPIView.as_view(), name="complete-rented"),
    path("contract-counter/", ContractCounter.as_view(), name="contract-counter")
]