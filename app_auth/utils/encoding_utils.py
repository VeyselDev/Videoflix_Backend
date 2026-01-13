from typing import Optional

from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_int_to_b64(value: int) -> str:
    return urlsafe_base64_encode(force_bytes(value))


def decode_b64_to_int(uidb64: str) -> Optional[int]:
    try:
        return int(force_str(urlsafe_base64_decode(uidb64)))
    except (TypeError, ValueError, OverflowError):
        return None
