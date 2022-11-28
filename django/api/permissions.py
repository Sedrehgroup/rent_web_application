from rest_framework.permissions import BasePermission
from users.models import User


class IsLandlord(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            contract_landlord = request.data.get('contract_landlord')
            landlord = User.objects.get(pk=contract_landlord)
            return landlord.id == request.user.id
        return True

    def has_object_permission(self, request, view, obj):
        return obj.contract_landlord_id == request.user.id


class IsTenant(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            contract_tenant = request.data.get('contract_tenant')
            tenant = User.objects.get(pk=contract_tenant)
            return tenant.id == request.user.id
        return True

    def has_object_permission(self, request, view, obj):
        return obj.contract_tenant_id == request.user.id


class TenantIsNotLandlord(BasePermission):
    message = 'owner and tenant are equal'

    def has_permission(self, request, view):
        if request.method == 'POST':

            contract_landlord = request.data.get('contract_landlord')
            contract_tenant = request.data.get('contract_tenant')

            landlord = User.objects.get(pk=contract_landlord)
            tenant = User.objects.get(pk=contract_tenant)

            return tenant.id != landlord.id
        return True


