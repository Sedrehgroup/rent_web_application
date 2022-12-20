from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from datetime import datetime, timezone
from utils import send_otp_code, phone_number_validator
from .models import OtpCode, User
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, CreateUserSerializer, \
    RetrieveUpdateDestroyUserSerializer, UserCompletionSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CreateUser(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer


class RetrieveUpdateDestroyUser(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveUpdateDestroyUserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class OtpRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        is_valid, msg = phone_number_validator(phone_number=phone_number)

        if not is_valid:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        random_code = random.randint(1000, 9999)
        send_otp_code(phone_number=phone_number, code=random_code)

        updated_values = {'code': f'{random_code}'}
        OtpCode.objects.update_or_create(phone_number=phone_number, defaults=updated_values)

        return Response(data=random_code, status=status.HTTP_200_OK)


class VerifyOtpRegister(DestroyAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        try:
            instance_code = OtpCode.objects.get(phone_number=phone_number, code=code)
            second_difference = (datetime.now(timezone.utc) - instance_code.created).total_seconds()

            if second_difference > 120:
                instance_code.delete()
                return Response(data={"token is expired"}, status=status.HTTP_403_FORBIDDEN)

            else:
                instance_code.delete()
                try:
                    user = User.objects.get(phone_number=phone_number)
                    token = RefreshToken.for_user(user)
                    data = {'refresh': str(token), "access": str(token.access_token)}
                    return Response(data, status=status.HTTP_200_OK)
                except:
                    return Response(data={"User is not created"}, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response(data={"otp code is wrong"}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUser(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        if self.kwargs["pk"] == self.request.user.id or self.request.user.is_admin:
            return self.request.user
        raise PermissionDenied("You don't have access to see the details of other account")


class IsUserCompletion(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCompletionSerializer
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        serializer =  self.serializer_class(user)
        not_complete_value = []
        for key, value in serializer.data.items():
            if not value:
                not_complete_value.append(key)
        if not_complete_value:
            return Response(not_complete_value, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_200_OK)
