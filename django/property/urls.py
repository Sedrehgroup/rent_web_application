from django.urls import path
from .views import PropertyList, CreateListMyProperties, RetrieveUpdateDestroyProperties


urlpatterns = [
    path('properties_list/', PropertyList().as_view()),
    path('my_properties/', CreateListMyProperties().as_view()),
    path('modify_properties/<int:pk>/', RetrieveUpdateDestroyProperties().as_view()),
]