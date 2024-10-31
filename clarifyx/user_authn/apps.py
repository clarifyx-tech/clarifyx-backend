import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserAuthnConfig(AppConfig):
    name = "clarifyx.user_authn"
    verbose_name = _("User Authentication")

    def ready(self):
        with contextlib.suppress(ImportError):
            import clarifyx.user_authn.signals  # noqa: F401
