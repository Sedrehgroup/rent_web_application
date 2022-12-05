from rest_framework import serializers
from .models import Request
from property.serializer import PropertySerializer
from account.serializers import RetrieveUpdateDestroyUserSerializer
from account.models import User


class CreateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        exclude = ('tenant',)


class RequestSerializer(serializers.ModelSerializer):
    request_property = PropertySerializer(read_only=True)
    tenant = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = "__all__"

    def get_tenant(self, obj):
        tenant = User.objects.get(id=obj.tenant_id)
        return RetrieveUpdateDestroyUserSerializer(instance=tenant).data


class LandlordUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('status',)
