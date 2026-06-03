from django.middleware.csrf import get_token

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app_auth.api.serializers import (
    UserRegistrationSerializer,
    PasswordChangeSerializer,
    UserLoginSerializer,
    UserSerializer
)
from app_auth.services.auth_service import (
    validate_user_or_fail,
    login_user,
    revoke_refresh_token,
    renew_tokens,
    get_cookie_kwargs,
    AuthCookie
)
from app_auth.services.email_service import EmailType, enqueue_email
from app_auth.services.user_service import create_user, get_user_or_404, activate_user


class UserRegistrationView(APIView):
    """
    Handles new user registration.

    Validates input data, creates a deactivated user instance, and triggers
    an activation email via an asynchronous queue.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request) -> Response:
        """
        Register a new user.

        Args:
            request (Request): Contains username, email, and password.

        Returns:
            Response: Serialized user data on success.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user(**serializer.validated_data)
        enqueue_email(email_type=EmailType.USER_ACTIVATION, user_id=user.pk)
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class UserActivationView(APIView):
    """
    Handles account activation via email link.

    Verifies the user identity and token validity before enabling the account.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request: Request, uidb64: str, token: str) -> Response:
        """
        Activate a user account.

        Args:
            request (Request): The GET request.
            uidb64 (str): Base64 encoded user ID.
            token (str): One-time activation token.

        Returns:
            Response: Success message or failure details.
        """
        try:
            user = get_user_or_404(uidb64=uidb64)
            validate_user_or_fail(user, token)
            activate_user(user)
            return Response(
                {"message": "Account successfully activated."},
                status=status.HTTP_200_OK
            )

        except AuthenticationFailed:
            return Response(
                {"message": "Activation failed."},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginView(APIView):
    """
    Handles user authentication and JWT issuance.

    On successful login, JWT tokens are stored in secure HttpOnly cookies.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request: Request) -> Response:
        """
        Authenticate user and set secure cookies.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access, refresh, user = login_user(
            serializer.validated_data["email"],
            serializer.validated_data["password"]
        )
        
        get_token(request)

        cookie_kwargs = get_cookie_kwargs()
        response = Response(
            {"detail": "Login successful", "user": UserSerializer(user).data},
            status=status.HTTP_200_OK
        )

        # Set HttpOnly cookies for security
        response.set_cookie(AuthCookie.ACCESS.value, access, **cookie_kwargs)
        response.set_cookie(AuthCookie.REFRESH.value, refresh, **cookie_kwargs)

        return response


class UserLogoutView(APIView):
    """
    Handles user logout.

    Revokes the refresh token in the backend and clears cookies on the client side.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Logout the user and invalidate tokens.
        """
        refresh_token = request.COOKIES.get(AuthCookie.REFRESH.value)
        revoke_refresh_token(refresh_token)

        response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie(AuthCookie.ACCESS.value)
        response.delete_cookie(AuthCookie.REFRESH.value)
        return response


class TokenRefreshView(APIView):
    """
    Refreshes the Access and Refresh JWT tokens.

    Expects the current refresh token to be present in the request cookies.
    """
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """
        Renew session tokens using a valid refresh token.
        """
        refresh_token = request.COOKIES.get(AuthCookie.REFRESH.value)
        access, refresh = renew_tokens(refresh_token)

        response = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)
        response.set_cookie(AuthCookie.ACCESS.value, access, **get_cookie_kwargs())
        response.set_cookie(AuthCookie.REFRESH.value, refresh, **get_cookie_kwargs())
        return response


class PasswordResetView(APIView):
    """
    Initiates the password reset process.

    Sends a reset link to the provided email if the user exists and is active.
    """
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """
        Request a password reset email.
        """
        email = request.data.get('email')
        user = get_user_or_404(email=email, is_active=True)
        enqueue_email(email_type=EmailType.PASSWORD_RESET, user_id=user.pk)

        return Response(
            {'detail': 'If an account exists, a reset email has been sent.'},
            status=status.HTTP_200_OK
        )


class PasswordChangeView(APIView):
    """
    Confirms password reset and updates the user's password.

    Requires a valid uidb64 and token sent via the password reset email.
    """
    permission_classes = [AllowAny]

    def post(self, request: Request, uidb64: str, token: str) -> Response:
        """
        Reset password using a token.
        """
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_or_404(uidb64=uidb64)
        validate_user_or_fail(user, token)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)