from datetime import timedelta

from django.utils import timezone

from app_auth.models import CustomUser


def delete_inactive_users(inactivity_days: int = 1):
    """
    Delete all users who have not activated their account within a
    defined inactivity period.
    """

    cutoff = timezone.now() - timedelta(days=inactivity_days)
    deleted_count, _ = CustomUser.objects.filter(is_active=False, created_at__lte=cutoff).delete()
    return f"Deleted {deleted_count} inactive users."