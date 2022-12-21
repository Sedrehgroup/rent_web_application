from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from chat.models import Note, Chat
from account.models import User


class ListCreateChatSerializer(serializers.ModelSerializer):
    property_title = serializers.SerializerMethodField(read_only=True)
    last_text = serializers.SerializerMethodField(read_only=True)

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        publisher= User.objects.get(id=ret["publisher"])
        tenant = User.objects.get(id=ret["tenant"])
        ret["publisher"] = {"id": publisher.id, "full_name": publisher.get_full_name()}
        ret["tenant"] = {"id": tenant.id, "full_name": tenant.get_full_name()}
        return ret

    def validate(self, attr):
        if attr["tenant"].id == attr["property"].owner_id:
            raise ValidationError({"tenant":"tenant ID is equal to publisher ID of property"})
        return attr

    def get_property_title(self, obj: Chat):
        return obj.property.title

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
