from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import OtpRegister, VerifyOtpRegister, CustomTokenObtainPairView, CreateUser, RetrieveUpdateDestroyAdditionalUserInformation, CreateAdditionalUserInformation

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('user_information/', RetrieveUpdateDestroyAdditionalUserInformation.as_view(), name='user_information'),
    path('create_user_information/', CreateAdditionalUserInformation.as_view(), name='create_user_information'),
    path('otp_register/', OtpRegister.as_view(), name='otp_register'),
    path('verify_otp_register/', VerifyOtpRegister.as_view(), name='verify_otp_register'),
]
