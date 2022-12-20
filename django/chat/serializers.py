from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from chat.models import Note, Chat


class ListCreateChatSerializer(serializers.ModelSerializer):
    property_title = serializers.SerializerMethodField(read_only=True)
    publisher = serializers.SerializerMethodField(read_only=True)
    tenant = serializers.SerializerMethodField(read_only=True)
    last_text = serializers.SerializerMethodField(read_only=True)

    def get_property_title(self, obj: Chat):
        return obj.property.title

    def get_tenant(self,obj:Chat):
        return {"id": obj.tenant_id,"full_name":obj.tenant.get_full_name()}

    def get_publisher(self, obj: Chat):
        return {"id": obj.publisher_id,"full_name":obj.publisher.get_full_name()}

    def get_last_text(self, obj: Chat):
        last_note = Note.objects.filter(chat=obj).order_by("-created_date").only("text").first()
        return last_note.text if last_note is not None else ""

    class Meta:
        model = Chat
        fields = ["id", "tenant", "property", "publisher",
                  "property_title", "publisher", "last_text"]


class ListCreateNotesByChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ["chat", "creator"]
