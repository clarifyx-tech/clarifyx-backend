import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, OneToOneField, CASCADE, DateField
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class User(AbstractUser):
    """
    Default custom user model.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    country_code = CharField(_("Country Code"), max_length=5, default="91")
    mobile_number = CharField(_("Mobile Number"), blank=True, null=True, max_length=10)

    OTP_LENGTH = 4

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()
        super(User, self).save(*args, **kwargs)

    @staticmethod
    def generate_username() -> str:
        """
        Generate a random username using UUID.
        """
        return str(uuid.uuid4())


class UserProfile(TimeStampedModel):
    """
    User profile model for storing user attributes.
    """

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Not Specified'),
    ]

    user = OneToOneField(to=User, verbose_name=_("User"), on_delete=CASCADE)
    gender = CharField(_("Gender"), max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = DateField(_("Date of Birth"), null=True, blank=True)

    class Meta:
        db_table = 'userprofile'
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return self.user.username
