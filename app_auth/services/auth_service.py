from enum import Enum
from typing import cast

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from app_auth.models.custom_user import CustomUser
from core.utils.logging_utils import log_warning


class AuthCookie(str, Enum):
    """
    Enum representing cookie names used for authentication tokens.
    """
    ACCESS = 'access_token'
    REFRESH = 'refresh_token'


def get_cookie_kwargs() -> dict[str, any]:
    """
    Returns default cookie configuration for auth tokens.

    - httponly: Prevents JavaScript access (security)
    - secure: Enabled in production (HTTPS only)
    - samesite: CSRF protection policy
    - path: Cookie scope
    """
    return {
        'httponly': True,
        'secure': not settings.DEBUG,
        'samesite': 'Lax',
        'path': '/'
    }


def login_user(email: str, password: str) -> tuple[str, str, CustomUser]:
    """
    Authenticates a user using email and password.

    Returns:
        tuple(access_token, refresh_token, user)

    Raises:
        AuthenticationFailed: If credentials are invalid.
    """
    user = authenticate(email=email, password=password)
    if not user:
        raise AuthenticationFailed("Invalid credentials")

    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    return access, str(refresh), user


def renew_tokens(refresh_token: str) -> tuple[str, str]:
    """
    Generates new access and refresh tokens using a valid refresh token.

    Process:
    - Validates and decodes the provided refresh token
    - Loads the associated active user
    - Blacklists the old refresh token
    - Issues new access and refresh tokens

    Returns:
        tuple(new_access_token, new_refresh_token)

    Raises:
        AuthenticationFailed: If token is missing, invalid, expired, or user not found.
    """
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
    """
    Blacklists (revokes) a refresh token if provided.

    Silently logs a warning if token is invalid or blacklisting fails.
    """
    if refresh_token:
        try:
            token = RefreshToken(cast(any, refresh_token))
            token.blacklist()
        except TokenError as e:
            log_warning(f'Token blacklisting failed: {e}')


def is_user_token_valid(user: CustomUser, token: str) -> bool:
    """
    Validates a token against a user using Django's default token generator.

    Returns:
        True if token is valid, otherwise False.
    """
    return default_token_generator.check_token(user, token)


def validate_user_or_fail(user: CustomUser, token: str) -> None:
    """
    Validates a user-token pair.

    Raises:
        AuthenticationFailed: If token is invalid or expired.
    """
    if not is_user_token_valid(user, token):
        raise AuthenticationFailed("Invalid or expired credentials")