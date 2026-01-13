from typing import Optional

from rest_framework.generics import get_object_or_404

from app_auth.models import CustomUser
from app_auth.utils.encoding_utils import decode_b64_to_int


def create_user(email: str, password: str) -> CustomUser:
    user = CustomUser.objects.create_user(email=email, password=password)
    return user


def activate_user(user: CustomUser) -> None:
    user.is_active = True
    user.save(update_fields=['is_active'])


def get_user_or_fail(uidb64: Optional[str] = None, user_id: Optional[int] = None) -> CustomUser:
    user_pk = user_id or (decode_b64_to_int(uidb64) if uidb64 else None)

    if not user_pk:
        raise ValueError("Either uidb64 or user_id must be provided")

    return get_object_or_404(CustomUser, pk=user_pk)