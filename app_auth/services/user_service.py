from rest_framework.exceptions import NotFound

from app_auth.models import CustomUser
from app_auth.utils.token_utils import decode_uid


def create_user(email: str, password: str) -> CustomUser:
    """

    """
    user = CustomUser.objects.create_user(email=email, password=password)
    return user


def activate_user(user: CustomUser) -> None:
    user.is_active = True
    user.save(update_fields=['is_active'])


def get_user_from_uid_or_fail(uidb64: str) -> CustomUser:
    """
    Decode uidb64 and return the user, or raise NotFound if not found.
    """
    uid = decode_uid(uidb64)
    if uid is None:
        raise NotFound("User not found")

    user = CustomUser.objects.filter(pk=uid).first()
    if not user:
        raise NotFound("User not found")
    return user