from django.urls import path
from .views import ListCreateContract, RetrieveUpdateDestroyContract

urlpatterns = [
    path('list_create_contract/', ListCreateContract().as_view()),
    path('modify_contract/<int:pk>/', RetrieveUpdateDestroyContract().as_view()),
]
