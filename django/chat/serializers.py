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
        ret["publisher"] = {"id": instance.publisher.id, "full_name": instance.publisher.get_full_name()}
        ret["tenant"] = {"id": instance.tenant.id, "full_name": instance.tenant.get_full_name()}
        return ret

    def validate(self, attr):
        tenant_id = attr["tenant"].id
        owner_id = attr["property"].owner_id
        if tenant_id == owner_id:
            raise serializers.ValidationError({"tenant": "tenant ID is equal to publisher ID of property"})
        if self.context["request"].user.id not in (tenant_id, owner_id):
            raise serializers.ValidationError({"user": "You are not none of tenant or publisher. You are a bad man."})
        return attr

    def get_property_title(self, obj: Chat):
        return obj.property.title

    def get_last_text(self, obj: Chat):
        last_note = Note.objects.filter(chat=obj).order_by("-created_date").only("text").first()
        return last_note.text if last_note is not None else ""

    def create(self, validated_data):
        tenant_id = validated_data["tenant"].id
        owner_id = validated_data["property"].owner_id
        chat = Chat.objects\
            .filter(tenant_id=tenant_id, publisher_id=owner_id)\
            .select_related("publisher", "tenant")\
            .first()
        if chat:
            return chat
        return super().create(validated_data)

    class Meta:
        model = Chat
        fields = ["id", "tenant", "property", "publisher",
                  "property_title", "publisher", "last_text"]


class ListCreateNotesByChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ["chat", "creator"]
