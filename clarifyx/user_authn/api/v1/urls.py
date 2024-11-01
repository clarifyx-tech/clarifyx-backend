from django.urls import path

from clarifyx.user_authn.api.v1 import views

urlpatterns = [
    path("mobile/send-otp", views.SendOTPView.as_view(), name="mobile-send-otp"),
]
