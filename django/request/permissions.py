from rest_framework.permissions import BasePermission
from property.models import Property


class IsNotOwner(BasePermission):
    message = 'you can not request to your own property'

    def has_permission(self, request, view):

        request_property_id = request.data.get('request_property')
        is_owner = Property.objects.filter(owner=request.user, id=request_property_id).exists()

        return not is_owner