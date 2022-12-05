from rest_framework.permissions import BasePermission
from chat.models import Chat


class IsTenant(BasePermission):
    def has_object_permission(self, request, view, obj: Chat):
        return request.user.id == obj.tenant_id


class IsPublisher(BasePermission):
    def has_object_permission(self, request, view, obj: Chat):
        return request.user.id == obj.publisher_id
