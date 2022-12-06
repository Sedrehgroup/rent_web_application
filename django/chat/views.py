from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsAdmin
from chat.serializers import ListCreateChatSerializer, ListCreateNotesByChatSerializer
from chat.models import Chat, Note
from chat.permissions import IsTenant, IsPublisher
from chat.pagination import NotePagination


class ListCreateChat(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListCreateChatSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        is_tenant = Q(tenant_id=user_id)
        is_owner = Q(publisher_id=user_id)
        return Chat.objects.filter(is_tenant | is_owner)


class ListCreateNotesByChat(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsTenant | IsPublisher | IsAdmin]
    serializer_class = ListCreateNotesByChatSerializer
    pagination_class = NotePagination

    def get_object(self):
        chat = Chat.objects \
            .filter(id=self.kwargs['pk']) \
            .only("id") \
            .order_by() \
            .first()
        if not chat:
            raise NotFound({"Chat": "Chat with given ID is not exists."})
        self.check_object_permissions(self.request, chat)
        return chat

    def get_queryset(self):
        chat = self.get_object()
        return Note.objects.filter(chat_id=chat.id).order_by("-created_date")

    def perform_create(self, serializer):
        serializer.save(chat=self.get_object(), creator=self.request.user)
