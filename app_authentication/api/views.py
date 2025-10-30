from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pass


class ActivateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        pass

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pass


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass


class TokenRefreshView(SimpleJWTTokenRefreshView):
    permission_classes = [AllowAny]


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pass


class PasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        pass
