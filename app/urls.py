from django.contrib import admin
from django.urls import path
from .views import *
# from rest_framework.authtoken import views

app_name = "app"

urlpatterns = [
    path('signup',Signup),
    path('login',Login.as_view(),name="login"),
    path('resned_otp',Resendotp.as_view(),name="resend_otp"),
    path('phone_otp_verification',PhoneOtpVerification.as_view(),name="resend_otp"),
    # path('api-token-auth/', views.obtain_auth_token),
]
