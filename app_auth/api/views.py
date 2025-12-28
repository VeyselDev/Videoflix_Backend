from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_auth.api.serializers import UserRegistrationSerializer, PasswordChangeSerializer, UserLoginSerializer, UserSerializer
from app_auth.models import CustomUser

from app_auth.services.auth_service import invalidate_refresh_token, REFRESH_COOKIE_NAME, login_user, refresh_tokens, \
    build_user_activation_link, set_auth_cookies, clear_auth_cookies, validate_user_token_or_fail
from app_auth.services.email_service import send_password_reset_email, send_user_activation_email
from app_auth.services.user_service import create_user, activate_user, get_user_from_uid_or_fail
from app_auth.utils.queue_utils import enqueue_job


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user(**serializer.validated_data)
        activation_link = build_user_activation_link(request, user)
        enqueue_job(send_user_activation_email, user, activation_link)
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class UserActivationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            user = get_user_from_uid_or_fail(uidb64)
            validate_user_token_or_fail(user, token)
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
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access, refresh, user = login_user(serializer.validated_data["email"], serializer.validated_data["password"])
        response = Response({ "detail": "Login successful", "user": UserSerializer(user).data }, status=status.HTTP_200_OK)
        set_auth_cookies(response, access, refresh)

        return response


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
        invalidate_refresh_token(refresh_token)
        response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        clear_auth_cookies(response)
        return response


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
        access, refresh = refresh_tokens(refresh_token)

        response = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)
        set_auth_cookies(response, access, refresh)
        return response


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email, is_active=True).first()
        if user:
            enqueue_job(send_password_reset_email, request, user)
        return Response({'detail': 'If an account exists, a reset email has been sent.'}, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_from_uid_or_fail(uidb64)
        validate_user_token_or_fail(user, token)
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)