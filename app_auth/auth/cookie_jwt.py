from typing import Optional, Tuple

from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import Token

from app_auth.models.custom_user import CustomUser
from app_auth.services.auth_service import AuthCookie


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class for JWT verification via HttpOnly cookies.

    This class extends the standard JWTAuthentication to look for the access
    token within the browser's cookies rather than the 'Authorization' header.
    This approach helps mitigate Cross-Site Scripting (XSS) risks.
    """

    def authenticate(self, request: Request) -> Optional[Tuple[CustomUser, Token]]:
        """
        Extract and validate the JWT from the request cookies.

        Args:
            request (Request): The incoming DRF request object.

        Returns:
            Optional[Tuple[CustomUser, Token]]: A tuple containing the authenticated user
            and the validated token if successful; None otherwise.

        Note:
            If the access cookie is missing or the token is invalid/expired,
            this method returns None, allowing DRF to either try other
            authentication classes or return a 401 Unauthorized response.
        """
        # Retrieve the raw token string from the specific authentication cookie
        raw_token = request.COOKIES.get(AuthCookie.ACCESS.value)

        if not raw_token:
            return None

        try:
            # Standard JWT validation (signature, expiration, etc.)
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError):
            # If token is corrupted or expired, fail silently to allow DRF handling
            return None

        # Return the user instance associated with the token and the token object itself
        return self.get_user(validated_token), validated_token