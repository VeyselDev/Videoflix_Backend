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


def get_user_or_404(
        uidb64: Optional[str] = None,
        pk: Optional[int] = None,
        email: Optional[str] = None,
        is_active: Optional[bool] = None
) -> CustomUser:

    filters = {}

    if pk:
        filters["pk"] = pk
    elif uidb64:
        filters["pk"] = decode_b64_to_int(uidb64)
    elif email:
        filters["email"] = email
    else:
        return get_object_or_404(CustomUser, pk=None)  # erzwingt 404

    if is_active is not None:
        filters["is_active"] = is_active

    return get_object_or_404(CustomUser, **filters)