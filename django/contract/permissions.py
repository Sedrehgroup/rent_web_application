from rest_framework.permissions import BasePermission
from account.models import User
from account.serializers import UserCompletionSerializer


class IsLandlord(BasePermission):
    message = 'you are not landlord'

    def has_permission(self, request, view):
        contract_landlord = request.data.get('contract_landlord')
        return contract_landlord == request.user.id


class IsTenant(BasePermission):
    message = 'you are not tenant'

    def has_permission(self, request, view):
        contract_tenant = request.data.get('contract_tenant')
        return contract_tenant == request.user.id


class ObjectIsLandlord(BasePermission):
    message = 'you are not landlord or tenant'

    def has_object_permission(self, request, view, obj):
        return obj.contract_landlord_id == request.user.id


class ObjectIsTenant(BasePermission):
    message = 'you are not landlord or tenant'

    def has_object_permission(self, request, view, obj):
        return obj.contract_tenant_id == request.user.id


class IsUserCompletePermission(BasePermission):
    message = ""
    
    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        serializer =  UserCompletionSerializer(user)
        not_complete_value = []
        for key, value in serializer.data.items():
            if not value:
                not_complete_value.append(key)
        if not_complete_value:
            self.message = " ".join(not_complete_value)
            return False
        return super().has_permission(request, view)
