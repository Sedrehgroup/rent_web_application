from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
"""class User(models.Model):
    FirstName = models.CharField(max_length=255)
    LastName = models.CharField(max_length=255)
    FatherName = models.CharField(max_length=255)
    NationalID = models.IntegerField(max_length=10, unique=True)

    def __str__(self):
        return self.NationalID"""


class Rent(models.Model):
    landlord = models.ForeignKey(User, related_name='rent_landlord', on_delete=models.PROTECT)
    tenant = models.ForeignKey(User, related_name='rent_tenant', on_delete=models.PROTECT)
    mortgage_amount = models.IntegerField()
    rent_amount = models.IntegerField()
    meterage = models.IntegerField()
    type = models.CharField(max_length=30)
    use = models.CharField(max_length=30)
    bedrooms = models.IntegerField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    zip = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.zip
