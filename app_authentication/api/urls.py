from django.urls import path
from .views import (
    RegisterView,
    ActivateView,
    LoginView,
    LogoutView,
    TokenRefreshView,
    PasswordResetView,
    PasswordConfirmView,
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/activate/<str:uidb64>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/password_confirm/<str:uidb64>/<str:token>/', PasswordConfirmView.as_view(), name='password_confirm'),
]
