from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Property(models.Model):

    # Primary Fields
    owner = models.ManyToManyField(User, related_name='owner')
    title = models.CharField(max_length=150)
    mortgage_amount = models.IntegerField()
    rent_amount = models.IntegerField()
    type = models.SmallIntegerField()
    use = models.SmallIntegerField()
    special_situation = models.SmallIntegerField(null=True)
    area = models.IntegerField()
    province = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    neighbourhood = models.CharField(max_length=100)
    convertible = models.BooleanField()
    construction_year = models.SmallIntegerField()
    bedrooms = models.SmallIntegerField()
    description = models.TextField(max_length=350, null=True)

    # Additional Fields
    zip = models.CharField(max_length=10, null=True)
    Sub_registration_plate = models.IntegerField(null=True)
    Sub_registration_plate_from = models.IntegerField(null=True)
    Sub_registration_plate_to = models.IntegerField(null=True)
    Original_registration_plate = models.IntegerField(null=True)
    Original_registration_plate_from = models.IntegerField(null=True)
    Original_registration_plate_to = models.IntegerField(null=True)
    registration_section = models.CharField(max_length=100, null=True)
    registration_area = models.CharField(max_length=100, null=True)
    Skeleton_type = models.SmallIntegerField(null=True)
    phone_status = models.SmallIntegerField(null=True)
    phone_lines = models.SmallIntegerField(null=True)
    address = models.CharField(max_length=250, null=True)
    building_side = models.SmallIntegerField(null=True)
    unit_side = models.SmallIntegerField(null=True)
    unit_floor = models.SmallIntegerField(null=True)
    floors_number = models.SmallIntegerField(null=True)
    units_per_floor = models.SmallIntegerField(null=True)


class Request(models.Model):
    request_property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='request_property')
    tenant = models.ForeignKey(User, on_delete=models.PROTECT, related_name='request_tenant')
    status = models.SmallIntegerField()
    tenant_description = models.CharField(max_length=350, null=True)
    landlord_description = models.CharField(max_length=350, null=True)


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

