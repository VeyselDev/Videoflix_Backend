import django_rq
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rq import Retry

from app_authentication.api.serializers import RegistrationSerializer
from app_authentication.models import CustomUser
from app_authentication.tasks import send_activation_email
from core import settings
from core.settings import COOKIE_SECURE


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_path = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
            activation_link = request.build_absolute_uri(activation_path)

            queue = django_rq.get_queue('default')
            queue.enqueue(send_activation_email, user, activation_link, retry=Retry(max=3), job_timeout=120)

            return Response({'user': {'id': user.id, 'email': user.email}}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ActivateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return render(request, 'authentication/activation_failed.html', status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'authentication/activation_success.html', status=200)
        else:
            return render(request, 'authentication/activation_failed.html', status=400)



class CookieTokenLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        refresh = response.data.get('refresh')
        access = response.data.get('access')

        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite='Lax' if settings.COOKIE_SECURE else None,
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite='Lax' if settings.COOKIE_SECURE else None,
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        response.data = {
            'detail': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username
            }
        }

        return response



class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is missing.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {'detail': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(
            {'detail': 'Logout successful! All tokens will be deleted. Refresh token is now invalid.'},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({'detail': 'Refresh token not found!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response({'detail': 'Refresh token invalid!'}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = serializer.validated_data.get('access')

        response = Response({'detail': 'Token refreshed', 'access': access_token})
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite='Lax' if settings.COOKIE_SECURE else None,
        )

        return response

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        users = CustomUser.objects.filter(email=email, is_active=True)
        if not users.exists():
            return Response({'detail': 'An email has been sent to reset your password.'}, status=status.HTTP_200_OK)

        for user in users:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_path = reverse('password_confirm', kwargs={'uidb64': uidb64, 'token': token})
            reset_link = request.build_absolute_uri(reset_path)

            html_message = render_to_string('emails/password_reset.html', {
                'user': user,
                'reset_link': reset_link,
            })

            send_mail(
                subject='Password reset - Videoflix',
                message='Click the link to reset your password.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )


        return Response({'detail': 'An email has been sent to reset your password.'}, status=status.HTTP_200_OK)


class PasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response(
                {'detail': 'Both new_password and confirm_password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {'detail': 'Passwords do not match.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response(
                {'detail': 'Invalid link.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {'detail': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {'detail': 'Your Password has been successfully reset.'},
            status=status.HTTP_200_OK
        )
