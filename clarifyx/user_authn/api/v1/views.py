from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from clarifyx.core.otp import OTPManager
from clarifyx.user_authn.api.v1.serializers import SendOTPSerializer, VerifyOTPSerializer, ResendOTPSerializer


class OTPViewBase(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = self.get_response_body(serializer)
        status_code = self.get_status_code()

        return Response(response_data, status=status_code)

    def get_response_body(self, serializer):  # noqa
        return serializer.validated_data

    def get_status_code(self):  # noqa
        return status.HTTP_200_OK


class SendOTPView(OTPViewBase):
    """
    **Description**
        Sends a one-time password (OTP) to a user's mobile number.

    **Example Request**
        POST /api/auth/v1/mobile/send-otp

    **Request Body**
        * `mobile_number`: string (required) - The mobile number to send the OTP.

    **Response**
        * 201 Created: OTP sent successfully.
        * 400 Bad Request: Invalid mobile number.
    """

    serializer_class = SendOTPSerializer

    def get_response_body(self, serializer):
        return {
            "message": "OTP sent successfully."
        }


class ResendOTPView(OTPViewBase):
    """
    **Description**
        Resends a one-time password (OTP) to a user's mobile number.

    **Example Request**
        POST /api/auth/v1/mobile/resend-otp

    **Request Body**
        * `mobile_number`: string (required) - The mobile number to send the OTP.

    **Response**
        * 201 Created: OTP resent successfully.
        * 400 Bad Request: Invalid mobile number.
        * 400 Bad Request: No OTP request found to retry otp.
        * 400 Bad Request: OTP retry count maxed out.
    """

    serializer_class = ResendOTPSerializer

    def get_response_body(self, serializer):
        return {
            "message": "OTP resent successfully."
        }


class VerifyOTPView(APIView):
    """
    **Description**
        Verifies a one-time password to a user's mobile number.
        If user already exists, generate an authorization token.

    **Example Request**
        POST /api/auth/v1/mobile/verify-otp

    **Request Body**
        * `mobile_number`: string (required) - The mobile number to verify.
        * `otp`: string (required) - The otp to verify.

    **Response**
        * 201 Created: OTP verified successfully.
        * 400 Bad Request: OTP expired.
        * 400 Bad Request: OTP doesn't match.
    """

    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile_number = serializer.data['mobile_number']
        otp = serializer.data['otp']

        otp_manager = OTPManager(mobile_number=mobile_number)
        otp_manager.verify_otp(otp=otp)
