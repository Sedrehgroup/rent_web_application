from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from account.serializers import RetrieveUpdateDestroyUserSerializer, UserCompletionSerializer
from .models import Contract
from account.models import User
from property.models import Property
from property.serializer import LeasePropertySerializer


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
    
    def update(self, instance, validated_data):
        tenant_signature = validated_data.get("tenant_signature")
        landlord_signature = validated_data.get("landlord_signature")

        if tenant_signature or landlord_signature:
            if tenant_signature:
                instance.tenant_signature = True
                instance.document_status = 2
            if landlord_signature:
                instance.landlord_signature = True
                instance.document_status = 1
            
            if instance.tenant_signature and instance.landlord_signature:
                instance.document_status = 3
        
        if instance.tenant_signature and tenant_signature==False:
            instance.document_status = 6
        elif instance.landlord_signature and landlord_signature==False:
            instance.document_status = 6

        if validated_data != {} and tenant_signature==None and landlord_signature==None:
            instance.document_status = 4

        return super().update(instance, validated_data)


class LeaseSerializer(serializers.ModelSerializer):
    contract_landlord = serializers.SerializerMethodField()
    contract_tenant = serializers.SerializerMethodField()
    contract_property = serializers.SerializerMethodField()
    class Meta:
        model = Contract
        fields = (
            "dong", "start_date", "end_date", "contract_landlord", "contract_tenant",
            "contract_property", "document_status",
        )
    def get_contract_landlord(self, obj):
        contract_landlord = User.objects.get(id=obj.contract_landlord_id)
        return UserCompletionSerializer(instance=contract_landlord).data

    def get_contract_tenant(self, obj):
        contract_tenant = User.objects.get(id=obj.contract_tenant_id)
        return UserCompletionSerializer(instance=contract_tenant).data

    def get_contract_property(self, obj):
        contract_property = Property.objects.get(id=obj.contract_property_id)
        return LeasePropertySerializer(instance=contract_property).data
