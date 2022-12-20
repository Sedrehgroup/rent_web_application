from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import OtpRegister, VerifyOtpRegister, CustomTokenObtainPairView, CreateUser,\
    RetrieveUpdateDestroyUser, IsUserCompletion

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('create_user/', CreateUser.as_view(), name='create_user'),
    path('user_information/', RetrieveUpdateDestroyUser.as_view(), name='user'),

    path('otp_register/', OtpRegister.as_view(), name='otp_register'),
    path('verify_otp_register/', VerifyOtpRegister.as_view(), name='verify_otp_register'),
    
    path("user-complete/", IsUserCompletion.as_view(), name="user-complete"),
]
