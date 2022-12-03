from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from .models import Contract
from account.models import User


class ContractSerializer(serializers.ModelSerializer):
    contract_landlord = serializers.SerializerMethodField()
    contract_tenant = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = "__all__"

    def get_contract_landlord(self, obj):
        contract_landlord = User.objects.filter(id=obj.contract_landlord_id).only("first_name", "last_name").first()
        return {"contract_landlord_id": contract_landlord.id, "first_name": contract_landlord.first_name, "last_name": contract_landlord.last_name}

    def get_contract_tenant(self, obj):
        contract_tenant = User.objects.filter(id=obj.contract_tenant_id).only("first_name", "last_name").first()
        return {"contract_landlord_id": contract_tenant.id, "first_name": contract_tenant.first_name, "last_name": contract_tenant.last_name}

    def validate(self, attrs):
        if self.context['request']._request.method == 'POST':
            if attrs['contract_landlord'] == attrs['contract_tenant']:
                raise ValidationError('owner and tenant are equal', status.HTTP_400_BAD_REQUEST)
            return attrs
        return attrs