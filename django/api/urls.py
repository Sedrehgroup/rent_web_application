from django.urls import path
from .views import RentList, RentDetail

urlpatterns = [
    path('rents/', RentList().as_view()),
    path('rents/<int:pk>', RentDetail().as_view()),
]
