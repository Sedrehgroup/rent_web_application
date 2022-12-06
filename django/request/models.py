from django.db import models
from django.conf import settings
from property.models import Property
User = settings.AUTH_USER_MODEL


class Request(models.Model):
    request_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='request_property')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_tenant')
    status = models.SmallIntegerField()
    tenant_description = models.CharField(max_length=350, null=True)
    landlord_description = models.CharField(max_length=350, null=True)

