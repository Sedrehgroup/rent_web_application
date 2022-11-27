from rest_framework.permissions import BasePermission


class IsLandlord(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.contract_landlord_id == request.user.id


class IsTenant(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.contract_tenant_id == request.user.id

