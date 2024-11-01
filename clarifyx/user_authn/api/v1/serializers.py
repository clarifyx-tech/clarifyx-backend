import re
from typing import Dict

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from clarifyx.core.otp import OTPManager
from clarifyx.user_authn.models import User


class MobileNumberSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=10, required=True)

    default_error_messages = {
        "invalid_mobile_number": _("Invalid mobile number."),
    }

    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        value = attrs.get('mobile_number')

        # Define a regex pattern for exactly 10 digits
        pattern = re.compile(r'^\d{10}$')

        if not pattern.match(value):
            self.fail("invalid_mobile_number")

        return attrs


class SendOTPSerializer(MobileNumberSerializer):

    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        data = super().validate(attrs)

        mobile_number = attrs.get('mobile_number')

        otp_manager = OTPManager(mobile_number=mobile_number)
        otp_manager.send_otp()

        return data


class ResendOTPSerializer(MobileNumberSerializer):

    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        data = super().validate(attrs)

        mobile_number = attrs.get('mobile_number')

        otp_manager = OTPManager(mobile_number=mobile_number)
        otp_manager.resend_otp()

        return data


class VerifyOTPSerializer(MobileNumberSerializer):
    otp = serializers.CharField(max_length=User.OTP_LENGTH, required=True)

    default_error_messages = {
        "invalid_otp_length": _("Invalid OTP length."),
    }

    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        data = super().validate(attrs)

        mobile_number = attrs.get('mobile_number')
        otp = attrs.get('otp')

        # Define a regex pattern for exactly 4 digits
        pattern = re.compile(r'^\d{User.OTP_LENGTH}$')

        if not pattern.match(otp):
            self.fail("invalid_otp_length")

        otp_manager = OTPManager(mobile_number=mobile_number)
        otp_manager.verify_otp(otp=otp)

        user = self.get_user(mobile_number=mobile_number)
        if user:


        return data

    def get_user(self, mobile_number: str) -> User or None:  # noqa
        try:
            return User.objects.get(mobile=mobile_number)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_token(cls, user: User) -> Token:
        return cls.token_class.for_user(user)  # type: ignore
