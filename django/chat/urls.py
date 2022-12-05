from django.urls import path

from chat.views import ListCreateChat, ListCreateNotesByChat

app_name = "chat"

urlpatterns = [
    path("", ListCreateChat.as_view(), name="list_chats"),
    path("<int:pk>/notes/", ListCreateNotesByChat.as_view(), name="list_notes_by_chat"),
]
