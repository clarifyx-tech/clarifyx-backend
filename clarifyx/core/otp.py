import json

from requests import post
from django.conf import settings
from rest_framework.exceptions import ValidationError


class OTPManager:

    base_uri = "https://control.msg91.com"

    def send_otp(self, country_code: str, mobile_number: str):
        if not settings.SEND_OTP_ENABLED:
            return

        uri = f"{self.base_uri}/api/v5/otp"
        params = {
            "otp_expiry": "5",
            "template_id": settings.MSG91_TEMPLATE_ID,  # TODO: get from msg91 panel and update it.
            "mobile": self.get_mobile(country_code=country_code, mobile_number=mobile_number),
            "authkey": settings.MSG91_AUTHKEY,
            "realTimeResponse": "1",
            "invisible": "1",
            "otp_length": "4",
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = post(uri, data=json.dumps(params), headers=headers)
        self.validate(status_code=response.status_code, response_json=response.json())

    def verify_otp(self, country_code: str, mobile_number: str, otp: str):
        if not settings.SEND_OTP_ENABLED:
            return

        uri = f"{self.base_uri}/api/v5/otp/verify"
        params = {
            "mobile": self.get_mobile(country_code=country_code, mobile_number=mobile_number),
            "otp": otp,
        }
        headers = {
            "authkey": settings.MSG91_AUTHKEY
        }

        response = post(uri, data=json.dumps(params), headers=headers)
        self.validate(status_code=response.status_code, response_json=response.json())

    @staticmethod
    def get_mobile(country_code: str, mobile_number: str) -> str:
        return f"{country_code}{mobile_number}"

    @staticmethod
    def validate(status_code: int, response_json: dict):
        if status_code != 200 or (status_code == 200 and response_json.get("type") == "error"):
            raise ValidationError(
                detail={
                    "non_field_errors": [response_json.get("message")]
                }
            )
