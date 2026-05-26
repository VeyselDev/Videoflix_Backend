from datetime import timedelta
from typing import Optional

from django.utils import timezone
from rest_framework.generics import get_object_or_404

from app_auth.models.custom_user import CustomUser
from app_auth.utils.encoding_utils import decode_b64_to_int


def create_user(email: str, password: str) -> CustomUser:
    """
    Creates a new user with the given email and password.

    Args:
        email: User email.
        password: Raw password.

    Returns:
        The created CustomUser instance.
    """
    user = CustomUser.objects.create_user(email=email, password=password)
    return user


def activate_user(user: CustomUser) -> None:
    """
    Activates a user account by setting is_active to True.

    Args:
        user: Target user instance.
    """
    user.is_active = True
    user.save(update_fields=['is_active'])


def get_user_or_404(
        uidb64: Optional[str] = None,
        pk: Optional[int] = None,
        email: Optional[str] = None,
        is_active: Optional[bool] = None
) -> CustomUser:
    """
    Retrieves a user by one of the supported identifiers or raises 404.

    Priority:
        1. pk
        2. uidb64 (decoded to pk)
        3. email

    Optionally filters by is_active.

    Args:
        uidb64: Base64 encoded user ID.
        pk: Primary key.
        email: User email.
        is_active: Optional active state filter.

    Returns:
        Matching CustomUser instance.

    Raises:
        Http404: If no matching user is found.
    """
    filters = {}

    if pk:
        filters["pk"] = pk
    elif uidb64:
        filters["pk"] = decode_b64_to_int(uidb64)
    elif email:
        filters["email"] = email
    else:
        return get_object_or_404(CustomUser, pk=None)

    if is_active is not None:
        filters["is_active"] = is_active

    return get_object_or_404(CustomUser, **filters)


def delete_inactive_users_older_than(hours: int) -> int:
    """
    Deletes inactive users older than a given number of hours.

    Args:
        hours: Age threshold in hours.

    Returns:
        Number of deleted user records.
    """
    cutoff = timezone.now() - timedelta(hours=hours)
    deleted_count, _ = (
        CustomUser.objects
        .filter(is_active=False, created_at__lte=cutoff)
        .delete()
    )
    return deleted_count