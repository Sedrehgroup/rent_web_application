from rest_framework import serializers
from .models import Request
from property.serializer import PropertySerializer


class CreateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        exclude = ('tenant',)


class RequestSerializer(serializers.ModelSerializer):
    request_property = PropertySerializer(read_only=True)

    class Meta:
        model = Request
        exclude = ('tenant',)


class LandlordUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('status',)
