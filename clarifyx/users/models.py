from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for ClarifyX.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]


class UserLoginAttempt(models.Model):
    """
    Model to track login attempts using OTP for users.
    """

    # The number of OTPs a user can use for a single login attempt.
    SEND_OTP_LIMIT = 5
    # If the SEND_OTP_LIMIT is reached, the user must wait for x hours before attempting to log in again.
    SEND_OTP_WAIT_TIME = timedelta(hours=24)
    # The number of retries a user can make for OTP verification during a single login attempt.
    VERIFY_OTP_LIMIT = 3
    # If the VERIFY_OTP_LIMIT is reached, the user will be redirected to log in and must wait for x hours before
    # attempting to log in again.
    VERIFY_OTP_WAIT_TIME = timedelta(hours=1)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="login")

    send_otp_attempts = models.PositiveIntegerField(default=0)
    send_otp_last_attempt = models.DateTimeField(null=True, blank=True)

    verify_otp_attempts = models.PositiveIntegerField(default=0)
    verify_otp_last_attempt = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "user_login_attempt"
        verbose_name = _("User Login Attempt")
        verbose_name_plural = _("User Login Attempts")

    @property
    def can_send_otp(self) -> bool:
        """
        Check if the user can attempt to log in.
        """
        now = timezone.now()
        has_reached_wait_time = now - self.send_otp_last_attempt > self.SEND_OTP_WAIT_TIME

        # noinspection PyTypeChecker
        return not (self.send_otp_attempts > self.SEND_OTP_LIMIT and not has_reached_wait_time)
