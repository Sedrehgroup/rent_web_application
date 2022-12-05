from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from account.serializers import RetrieveUpdateDestroyUserSerializer
from account.serializers import CreateAdditionalUserInformationSerializer
from .models import Contract
from account.models import User, UserAdditionalInformation


class ContractSerializer(serializers.ModelSerializer):
    contract_landlord = serializers.SerializerMethodField()
    contract_landlord_information = serializers.SerializerMethodField()
    contract_tenant = serializers.SerializerMethodField()
    contract_tenant_information = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = "__all__"

    def get_contract_landlord(self, obj):
        contract_landlord = User.objects.get(id=obj.contract_landlord_id)
        return RetrieveUpdateDestroyUserSerializer(instance=contract_landlord).data

    def get_contract_landlord_information(self, obj):
        contract_landlord_information = UserAdditionalInformation.objects.get(user_id=obj.contract_landlord_id)
        return CreateAdditionalUserInformationSerializer(instance=contract_landlord_information).data


    def get_contract_tenant(self, obj):
        contract_tenant = User.objects.get(id=obj.contract_tenant_id)
        return RetrieveUpdateDestroyUserSerializer(instance=contract_tenant).data

    def get_contract_tenant_information(self, obj):
        contract_tenant_information = UserAdditionalInformation.objects.get(user_id=obj.contract_tenant_id)
        return CreateAdditionalUserInformationSerializer(instance=contract_tenant_information).data


    def validate(self, attrs):
        if self.context['request']._request.method == 'POST':
            if attrs['contract_landlord'] == attrs['contract_tenant']:
                raise ValidationError('owner and tenant are equal', status.HTTP_400_BAD_REQUEST)
            return attrs
        return attrs