from .models import User, OtpCode, UserAdditionalInformation
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from utils import phone_number_validator


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ("date_joined", "password", "groups", "user_permissions")

#
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(default='rent')
    class Meta:
        model = User
        fields = ("phone_number", "national_code", "first_name", "last_name", "password")

    def validate(self, attrs):
        is_valid, msg = phone_number_validator(attrs["phone_number"])
        if not is_valid:
            raise ValidationError({"phone_number": msg}, status.HTTP_400_BAD_REQUEST)
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        if password is not None:
            validated_data['password'] = make_password(password)
        return super(CreateUserSerializer, self).create(validated_data)

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        data = {'refresh': str(token), "access": str(token.access_token)}
        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        is_valid, msg = phone_number_validator(attrs["phone_number"])
        if not is_valid:
            raise AuthenticationFailed({"phone_number": msg})

        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        return data


class RetrieveUpdateDestroyAdditionalUserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdditionalInformation
        fields = "__all__"

class CreateAdditionalUserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdditionalInformation
        exclude = ('user', )