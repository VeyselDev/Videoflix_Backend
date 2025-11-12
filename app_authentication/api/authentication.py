from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        cookie_name = 'access_token'
        raw_token = request.COOKIES.get(cookie_name)

        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError, Exception):
            return None

        return self.get_user(validated_token), validated_token
