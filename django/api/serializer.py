from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from .models import Property, Request, Contract


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ('owner',)


class CreateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        exclude = ('tenant',)


class RequestSerializer(serializers.ModelSerializer):
    request_property = PropertySerializer(read_only=True)

    class Meta:
        model = Request
        exclude = ('tenant',)


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

    def validate(self, attrs):
        if attrs['contract_landlord'] == attrs['contract_tenant']:
            raise ValidationError('owner and tenant are equal', status.HTTP_400_BAD_REQUEST)
        return attrs
