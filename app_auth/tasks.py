from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from app_auth.models import CustomUser


def delete_inactive_users(inactivity_seconds: int = settings.PASSWORD_RESET_TIMEOUT) -> str:
    """
    Delete all users who have not activated their account within a
    defined inactivity period.
    """

    cutoff = timezone.now() - timedelta(seconds=inactivity_seconds)
    deleted_count, _ = CustomUser.objects.filter(is_active=False, created_at__lte=cutoff).delete()
    return f"Deleted {deleted_count} inactive users."