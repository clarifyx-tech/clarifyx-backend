import re

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from clarifyx.user_authn.models import User


class MobileNumberSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10, required=True)

    default_error_messages = {
        "invalid_mobile_number": _("Invalid mobile number."),
    }

    def validate_mobile_number(self, value):
        # Define a regex pattern for exactly 10 digits
        pattern = re.compile(r'^\d{10}$')

        if not pattern.match(value):
            self.fail("invalid_mobile_number")

        return value


class SendOTPSerializer(MobileNumberSerializer):
    pass


class VerifyOTPSerializer(MobileNumberSerializer):
    otp = serializers.CharField(max_length=User.OTP_LENGTH, required=True)

    default_error_messages = {
        "invalid_otp_length": _("Invalid OTP length."),
    }

    def validate_otp(self, value):
        # Define a regex pattern for exactly 4 digits
        pattern = re.compile(r'^\d{User.OTP_LENGTH}$')

        if not pattern.match(value):
            self.fail("invalid_otp_length")

        return value


class ResendOTPSerializer(MobileNumberSerializer):
    pass
