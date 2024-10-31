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
            "mobile": f"{country_code}{mobile_number}",
            "authkey": settings.MSG91_AUTHKEY,
            "realTimeResponse": "1",
            "invisible": "1",
            "otp_length": "4",
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = post(uri, data=json.dumps(params), headers=headers)
        data = response.json()

        if response.status_code != 200 or (response.status_code == 200 and data.get("type") == "error"):
            raise ValidationError(
                detail={
                    "non_field_errors": [response.json().get("message")]
                }
            )
