from rest_framework import serializers
from .models import Property
from account.models import User


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = "__all__"

    def get_owner(self, obj):
        owner = User.objects.filter(id=obj.owner_id).only("first_name", "last_name").first()
        return {"owner_id": owner.id, "first_name": owner.first_name, "last_name": owner.last_name}


class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ("id" ,"title", "mortgage_amount", "rent_amount",
         "county", "city", "province", "area")
