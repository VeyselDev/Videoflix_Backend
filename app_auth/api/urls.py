from django.urls import path

from .views import (
    UserRegistrationView,
    UserActivationView,
    UserLogoutView,
    PasswordResetRequestView,
    PasswordChangeView, TokenRefreshView, UserLoginView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', UserActivationView.as_view(), name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_confirm/<str:uidb64>/<str:token>/', PasswordChangeView.as_view(), name='password_confirm'),
]