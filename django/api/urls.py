from django.urls import path
from .views import PropertyList, CreateListMyProperties, RetrieveUpdateDestroyProperties, CreateListRequests, \
    ListRequestsToMe, RetrieveUpdateDestroyRequests, ListCreateContract, RetrieveUpdateDestroyContract

urlpatterns = [
    path('properties_list/', PropertyList().as_view()),
    path('my_properties/', CreateListMyProperties().as_view()),
    path('modify_properties/<int:pk>/', RetrieveUpdateDestroyProperties().as_view()),

    path('requests/', CreateListRequests().as_view()),
    path('requests_to_me/', ListRequestsToMe().as_view()),
    path('modify_requests/<int:pk>/', RetrieveUpdateDestroyRequests().as_view()),

    path('list_create_contract/', ListCreateContract().as_view()),
    path('modify_contract/<int:pk>/', RetrieveUpdateDestroyContract().as_view()),
]
