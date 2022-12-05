from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/property/', include('property.urls')),
    path('api/request/', include('request.urls')),
    path('api/contract/', include('contract.urls')),
    path('api/chat/', include('chat.urls')),
    path('account/', include('account.urls')),

]
