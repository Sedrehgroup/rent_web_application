from django.db import models
from django.conf import settings
from django.utils.timezone import now
User = settings.AUTH_USER_MODEL


class Property(models.Model):

    # Primary Fields
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
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
    created_date = models.DateTimeField(default=now)
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
