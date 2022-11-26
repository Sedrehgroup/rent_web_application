from django.urls import path
from .views import PropertyList, CreateListMyProperties

urlpatterns = [
    path('properties_list/', PropertyList().as_view()),
    path('my_properties/', CreateListMyProperties().as_view()),
]
