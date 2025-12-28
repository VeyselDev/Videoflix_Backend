from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from app_auth.services.auth_service import ACCESS_COOKIE_NAME


class CookieJWTAuthentication(JWTAuthentication):
    """
    JWT auth via HttpOnly cookies instead of the Authorization header
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get(ACCESS_COOKIE_NAME)

        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError):
            return None

        return self.get_user(validated_token), validated_token
