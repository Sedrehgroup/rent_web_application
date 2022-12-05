from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user:
            return False
        return user.is_staff and user.is_superuser
