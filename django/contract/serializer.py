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
        if self.context['request'].method == 'POST':
            if data['contract_landlord'] == data['contract_tenant']:
                raise ValidationError('owner and tenant are equal', status.HTTP_400_BAD_REQUEST)
            return data

        return data
    
    def get_status_and_signatures(self, instance, validated_data):
        tenant_signature = validated_data.pop("tenant_signature", None)
        landlord_signature = validated_data.pop("landlord_signature", None)
        user = self.context['request'].user

        last_tenant_signature = instance.tenant_signature
        last_landlord_signature = instance.landlord_signature
        document_status = instance.document_status

        if validated_data != {} and tenant_signature==None and landlord_signature==None:
            document_status = 4

        else:
            if landlord_signature != None and user.id == instance.contract_landlord_id:
                if landlord_signature and not instance.landlord_signature:
                    last_landlord_signature = True
                    document_status = 1

                elif instance.landlord_signature and landlord_signature==False:
                    last_landlord_signature = False
                    document_status = 6

            elif tenant_signature != None and user.id == instance.contract_tenant_id:
                if tenant_signature and not instance.tenant_signature:
                    last_tenant_signature = True
                    document_status = 2
    
                elif instance.tenant_signature and tenant_signature==False:
                    last_tenant_signature = False
                    document_status = 6

            if last_tenant_signature and last_landlord_signature:
                document_status = 3

        return (document_status, last_landlord_signature, last_tenant_signature)

    def update(self, instance, validated_data):
        status_and_signatures = self.get_status_and_signatures(instance, validated_data)

        instance.document_status = status_and_signatures[0]
        instance.landlord_signature = status_and_signatures[1]
        instance.tenant_signature = status_and_signatures[2]
        return super().update(instance, validated_data)


class LeaseSerializer(serializers.ModelSerializer):
    contract_landlord_information = serializers.SerializerMethodField()
    contract_tenant_information  = serializers.SerializerMethodField()
    contract_property_information = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        exclude = (
            "contract_registration_date", "serial_type", "serial_number", 
            "tenant_signature", "landlord_signature"
            )
        extra_kwargs = {
            'contract_tenant': {'write_only': True},
            'contract_landlord': {'write_only': True},
            "contract_property": {'write_only': True},
        }

    def get_contract_landlord_information(self, obj):
        contract_landlord = User.objects.get(id=obj.contract_landlord_id)
        return UserCompletionSerializer(instance=contract_landlord).data

    def get_contract_tenant_information(self, obj):
        contract_tenant = User.objects.get(id=obj.contract_tenant_id)
        return UserCompletionSerializer(instance=contract_tenant).data

    def get_contract_property_information(self, obj):
        contract_property = Property.objects.get(id=obj.contract_property_id)
        return LeasePropertySerializer(instance=contract_property).data
