from rest_framework import serializers
from chat.models import Note, Chat


class CustomListChatSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        list_data = super().to_representation(data)
        return sorted(list_data, key=lambda d: d['last_note']['date'] if d['last_note'] else '', reverse=True)


class ListCreateChatSerializer(serializers.ModelSerializer):
    property_title = serializers.SerializerMethodField(read_only=True)
    last_note = serializers.SerializerMethodField(read_only=True)

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

    def get_last_note(self, obj: Chat):
        last_note = Note.objects.filter(chat=obj).order_by("-created_date").only("text", "created_date").first()
        if last_note:
            return {"text": last_note.text, "date": last_note.created_date}
        return {"text": '', "date": obj.created_date}

    def create(self, validated_data):
        tenant_id = validated_data["tenant"].id
        owner_id = validated_data["property"].owner_id
        chat = Chat.objects \
            .filter(tenant_id=tenant_id, publisher_id=owner_id) \
            .select_related("publisher", "tenant") \
            .first()
        if chat:
            return chat
        return super().create(validated_data)

    class Meta:
        model = Chat
        list_serializer_class = CustomListChatSerializer
        fields = ["id", "tenant", "property", "publisher",
                  "property_title", "publisher", "last_note"]


class ListCreateNotesByChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ["chat", "creator"]
