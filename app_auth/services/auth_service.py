import logging
from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from app_auth.models import CustomUser
from app_auth.utils.token_utils import encode_uid

logger = logging.getLogger(__name__)

ACCESS_TOKEN_KEY = 'access'
REFRESH_TOKEN_KEY = 'refresh'

ACCESS_COOKIE_NAME = 'access_token'
REFRESH_COOKIE_NAME = 'refresh_token'


def login_user(email: str, password: str):
    user = authenticate(email=email, password=password)

    if not user:
        raise AuthenticationFailed("Invalid credentials")

    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    return access, str(refresh), user


def refresh_tokens(refresh_token: str) -> tuple[str, str]:
    if not refresh_token:
        raise AuthenticationFailed("Refresh token missing")

    try:
        old_refresh = RefreshToken(refresh_token) # type: ignore
        user_id = old_refresh.payload.get('user_id')
        user = CustomUser.objects.get(id=user_id)
    except (TokenError, ObjectDoesNotExist):
        raise AuthenticationFailed("Invalid or expired refresh token")

    old_refresh.blacklist()

    new_refresh = RefreshToken.for_user(user)
    new_access = new_refresh.access_token

    return str(new_access), str(new_refresh)

def invalidate_refresh_token(refresh_token: Optional[str]) -> None:
    if refresh_token:
        try:
            RefreshToken(refresh_token).blacklist() # type: ignore
        except TokenError as e:
            logger.warning(f'Token blacklisting failed: {e}')


def get_cookie_kwargs():
    return {
        'httponly': True,
        'secure': not settings.DEBUG,
        'samesite': 'Lax',
    }

def get_refresh_token_from_cookies(request):
    """
    Extract refresh token from request cookies.
    Returns None if not found.
    """
    return request.COOKIES.get(REFRESH_COOKIE_NAME)

def set_auth_cookies(response, access, refresh=None):
    kwargs = get_cookie_kwargs()
    response.set_cookie(ACCESS_COOKIE_NAME, access, **kwargs)
    if refresh:
        response.set_cookie(REFRESH_COOKIE_NAME, refresh, **kwargs)
    return response


def clear_auth_cookies(response):
    response.delete_cookie(ACCESS_COOKIE_NAME)
    response.delete_cookie(REFRESH_COOKIE_NAME)
    return response


def build_user_activation_link(request, user):
    """
    Build absolute activation URL for a given user.
    """
    uidb64 = encode_uid(user)
    token = default_token_generator.make_token(user)
    path = f'{settings.FRONTEND_USER_ACTIVATION_URL}?uid={uidb64}&token={token}'
    #path = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
    return request.build_absolute_uri(path)


def is_user_token_valid(user, token):
    return default_token_generator.check_token(user, token)

def build_password_reset_link(request, user):
    """
    Build absolute password reset URL.
    """
    uidb64 = encode_uid(user)
    token = default_token_generator.make_token(user)
    path = reverse('password_confirm', kwargs={'uidb64': uidb64, 'token': token})
    return request.build_absolute_uri(path)


def validate_user_token_or_fail(user, token) -> None:
    if token is None or not is_user_token_valid(user, token):
        raise AuthenticationFailed("Invalid or expired credentials")