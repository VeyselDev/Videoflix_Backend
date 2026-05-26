from typing import Optional

from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_int_to_b64(value: int) -> str:
    """
    Encodes an integer into a URL-safe Base64 string.

    Uses Django utilities to ensure proper byte conversion and encoding.

    Args:
        value: Integer to encode.

    Returns:
        URL-safe Base64 encoded string.
    """
    return urlsafe_base64_encode(force_bytes(value))


def decode_b64_to_int(uidb64: str) -> Optional[int]:
    """
    Decodes a URL-safe Base64 string back into an integer.

    Handles invalid input safely by returning None instead of raising errors.

    Args:
        uidb64: Base64 encoded string.

    Returns:
        Decoded integer if valid, otherwise None.
    """
    try:
        return int(force_str(urlsafe_base64_decode(uidb64)))
    except (TypeError, ValueError, OverflowError):
        return None