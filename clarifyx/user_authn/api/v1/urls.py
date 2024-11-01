from django.urls import path

from clarifyx.user_authn.api.v1 import views

urlpatterns = [
    path("mobile/send-otp", views.SendOTPView.as_view(), name="mobile-send-otp"),
    path("mobile/resend-otp", views.ResendOTPView.as_view(), name="mobile-resend-otp"),
    path("mobile/verify-otp", views.VerifyOTPView.as_view(), name="mobile-verify-otp"),
]
