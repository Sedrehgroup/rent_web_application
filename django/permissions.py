from rest_framework.permissions import BasePermission
from property.models import Property


class IsNotOwner(BasePermission):
    message = 'you can not request to your own property'

    def has_permission(self, request, view):

        request_property_id = request.data.get('request_property')
        is_owner = Property.objects.filter(owner=request.user, id=request_property_id).exists()

        return not is_owner


class IsLandlord(BasePermission):
    message = 'you are not landlord or tenant'

    def has_permission(self, request, view):
        contract_landlord = request.data.get('contract_landlord')
        return contract_landlord == request.user.id


class IsTenant(BasePermission):
    message = 'you are not landlord or tenant'

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
