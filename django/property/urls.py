from django.urls import path
from .views import PropertyList, CreateMyProperties, RetrieveUpdateDestroyProperties, RetrieveProperties, ListMyProperties


urlpatterns = [
    path('properties_list/', PropertyList().as_view()),
    path('properties_list/<int:pk>/', RetrieveProperties().as_view()),
    path('my_properties/', CreateMyProperties().as_view()),
    path('my_properties_list/', ListMyProperties().as_view()),
    path('modify_properties/<int:pk>/', RetrieveUpdateDestroyProperties().as_view()),
]