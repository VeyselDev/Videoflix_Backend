"""
URL configuration for the authentication module.

This module defines the API endpoints for user account management,
including registration, email activation, session management (JWT),
and password recovery flows.
"""

from django.urls import path

from .views import (
    UserRegistrationView,
    UserActivationView,
    UserLogoutView,
    PasswordResetView,
    PasswordChangeView,
    TokenRefreshView,
    UserLoginView,
)

urlpatterns = [
    # --- User Account Management ---
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', UserActivationView.as_view(), name='activate'),

    # --- Authentication & Session ---
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- Password Recovery Flow ---
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_confirm/<str:uidb64>/<str:token>/', PasswordChangeView.as_view(), name='password_confirm')
]