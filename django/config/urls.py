from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/property/', include('property.urls')),
    path('api/request/', include('request.urls')),
    path('api/contract/', include('contract.urls')),
    path('api/chat/', include('chat.urls')),
    path('account/', include('account.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
