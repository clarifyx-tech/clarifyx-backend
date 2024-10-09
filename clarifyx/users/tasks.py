from celery import shared_task

from .models import User


# TODO: take refer
@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()
