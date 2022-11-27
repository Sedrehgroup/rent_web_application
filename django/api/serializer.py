from rest_framework import serializers
from .models import Property, Request, Contract


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ('owner',)


class RequestSerializer(serializers.ModelSerializer):
    request_property = PropertySerializer()
    class Meta:
        model = Request
        exclude = ('tenant',)


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ('tenant',)
        # # exclude = ('owner',)