from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))


def decode_uid(uidb64):
    try:
        return force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError):
        return None
