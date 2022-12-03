from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

    def validate(self, attrs):
        if self.context['request']._request.method == 'POST':
            if attrs['contract_landlord'] == attrs['contract_tenant']:
                raise ValidationError('owner and tenant are equal', status.HTTP_400_BAD_REQUEST)
            return attrs
        return attrs