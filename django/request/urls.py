from django.urls import path
from .views import CreateListRequests, ListRequestsToMe, RetrieveUpdateDestroyRequests, LandlordUpdateRequest

urlpatterns = [
    path('my_requests/', CreateListRequests().as_view()),
    path('requests_to_me/', ListRequestsToMe().as_view()),
    path('modify_requests/<int:pk>/', RetrieveUpdateDestroyRequests().as_view()),
    path('modify_requests_to_me/<int:pk>/', LandlordUpdateRequest().as_view()),
]
