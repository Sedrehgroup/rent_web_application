from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = None
    phone_number = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=128)  # default = rent
    national_code = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number


class UserAdditionalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True, null=True)
    father_name = models.CharField(max_length=128, null=True)
    certificate_number = models.CharField(max_length=10, null=True)
    birth_day = models.DateField(null=True)
    sex = models.BooleanField(null=True)
    latin_first_name = models.CharField(max_length=100, null=True)
    latin_last_name = models.CharField(max_length=100, null=True)
    certificate_country = models.CharField(max_length=30, null=True)
    certificate_province = models.CharField(max_length=30, null=True)
    certificate_county = models.CharField(max_length=30, null=True)
    certificate_type = models.CharField(max_length=30, null=True)
    marriage = models.BooleanField(null=True)
    education = models.CharField(max_length=30, null=True)
    province = models.CharField(max_length=30, null=True)
    county = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    address = models.TextField(max_length=200, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    personal_phone_number = models.CharField(max_length=11, null=True, unique=True)


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=13, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'

