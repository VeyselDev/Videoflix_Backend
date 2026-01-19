import logging
from enum import Enum
from typing import cast, Tuple, Dict, Optional

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from app_auth.models import CustomUser


logger = logging.getLogger(__name__)


class AuthCookie(str, Enum):
    ACCESS = 'access_token'
    REFRESH = 'refresh_token'


def login_user(email: str, password: str) -> Tuple[str, str, CustomUser]:
    user = authenticate(email=email, password=password)
    if not user:
        raise AuthenticationFailed("Invalid credentials")

    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    return access, str(refresh), user


def renew_tokens(refresh_token: str) -> Tuple[str, str]:
    if not refresh_token:
        raise AuthenticationFailed("Refresh token missing")

    try:
        old_refresh = RefreshToken(cast(any, refresh_token))
        user_id = old_refresh.payload.get('user_id')
        user = CustomUser.objects.get(id=user_id, is_active=True)
    except (TokenError, ObjectDoesNotExist):
        raise AuthenticationFailed("Invalid or expired refresh token")

    old_refresh.blacklist()
    new_refresh = RefreshToken.for_user(user)
    new_access = new_refresh.access_token
    return str(new_access), str(new_refresh)


def revoke_refresh_token(refresh_token: str) -> None:
    if refresh_token:
        try:
            token = RefreshToken(cast(any, refresh_token))
            token.blacklist()
        except TokenError as e:
            logger.warning(f'Token blacklisting failed: {e}')


def _get_cookie_kwargs() -> Dict[str, any]:
    return {
        'httponly': True,
        'secure': not settings.DEBUG,
        'samesite': 'Lax',
        'path': '/'
    }


def set_auth_cookies(response: Response, access: str, refresh: Optional[str] = None) -> Response:
    kwargs = _get_cookie_kwargs()
    response.set_cookie(AuthCookie.ACCESS, access, **kwargs)
    if refresh:
        response.set_cookie(AuthCookie.REFRESH, refresh, **kwargs)
    return response


def clear_auth_cookies(response: Response) -> Response:
    response.delete_cookie(AuthCookie.ACCESS)
    response.delete_cookie(AuthCookie.REFRESH)
    return response


def is_user_token_valid(user: CustomUser, token: str) -> bool:
    return default_token_generator.check_token(user, token)


def validate_user_or_fail(user: CustomUser, token: str) -> None:
    if not is_user_token_valid(user, token):
        raise AuthenticationFailed("Invalid or expired credentials")