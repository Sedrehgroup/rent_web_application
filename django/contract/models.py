from django.db import models
from django.conf import settings
from property.models import Property
User = settings.AUTH_USER_MODEL


class Contract(models.Model):
    contract_landlord = models.ForeignKey(User, related_name='contract_landlord', on_delete=models.PROTECT)
    contract_tenant = models.ForeignKey(User, related_name='contract_tenant', on_delete=models.PROTECT)
    contract_property = models.OneToOneField(Property, related_name='contract_property', on_delete=models.PROTECT)
    contract_registration_date = models.DateField()
    contract_date = models.DateField()
    serial_type = models.SmallIntegerField(null=True)
    serial_number = models.IntegerField(null=True)
    document_status = models.SmallIntegerField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    share = models.SmallIntegerField()
    dong = models.SmallIntegerField()
