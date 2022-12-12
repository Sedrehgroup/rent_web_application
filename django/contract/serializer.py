from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from account.serializers import RetrieveUpdateDestroyUserSerializer
from .models import Contract
from account.models import User


class ContractSerializer(serializers.ModelSerializer):
    contract_landlord_information = serializers.SerializerMethodField()
    contract_tenant_information  = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = "__all__"
        extra_kwargs = {
            'contract_tenant': {'write_only': True},
            'contract_landlord': {'write_only': True},
        }

    def get_contract_landlord_information(self, obj):
        contract_landlord = User.objects.get(id=obj.contract_landlord_id)
        return RetrieveUpdateDestroyUserSerializer(instance=contract_landlord).data

    def get_contract_tenant_information(self, obj):
        contract_tenant = User.objects.get(id=obj.contract_tenant_id)
        return RetrieveUpdateDestroyUserSerializer(instance=contract_tenant).data

    def validate(self, data):
        if self.context['request']._request.method == 'POST':
            if data['contract_landlord'] == data['contract_tenant']:
                raise ValidationError('owner and tenant are equal', status.HTTP_400_BAD_REQUEST)
            return data
        return data
