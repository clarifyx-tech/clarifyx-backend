import json

from requests import post, get
from django.conf import settings
from rest_framework.exceptions import ValidationError

from clarifyx.user_authn.models import User


class OTPManager:

    base_uri = "https://control.msg91.com"

    def __init__(self, country_code: str, mobile_number: str):
        self.mobile_number = f"{country_code}{mobile_number}"

    def send_otp(self):
        if not settings.SEND_OTP_ENABLED:
            return

        uri = f"{self.base_uri}/api/v5/otp"
        params = {
            "otp_expiry": "5",
            "template_id": settings.MSG91_TEMPLATE_ID,  # TODO: get from msg91 panel and update it.
            "mobile": self.mobile_number,
            "authkey": settings.MSG91_AUTHKEY,
            "realTimeResponse": "1",
            "invisible": "1",
            "otp_length": str(User.OTP_LENGTH),
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = post(uri, data=json.dumps(params), headers=headers)
        self.validate(status_code=response.status_code, response_json=response.json())

    def verify_otp(self, otp: int):
        if not settings.SEND_OTP_ENABLED:
            return

        uri = f"{self.base_uri}/api/v5/otp/verify"
        params = {
            "mobile": self.mobile_number,
            "otp": otp,
        }
        headers = {
            "authkey": settings.MSG91_AUTHKEY
        }

        response = get(uri, data=json.dumps(params), headers=headers)
        self.validate(status_code=response.status_code, response_json=response.json())

    def resend_otp(self):
        if not settings.SEND_OTP_ENABLED:
            return

        uri = f"{self.base_uri}/api/v5/otp/retry"
        params = {
            "mobile": self.mobile_number,
            "retrytype": "Voice",
            "authkey": settings.MSG91_AUTHKEY
        }
        response = get(uri, data=json.dumps(params))
        self.validate(status_code=response.status_code, response_json=response.json())

    @staticmethod
    def validate(status_code: int, response_json: dict):
        if status_code != 200 or (status_code == 200 and response_json.get("type") == "error"):
            raise ValidationError(
                detail={
                    "non_field_errors": [response_json.get("message")]
                }
            )
