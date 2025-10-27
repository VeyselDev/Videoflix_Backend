from django.urls import path
from .views import (
    RegisterView,
    ActivateView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/activate/<str:uidb64>/<str:token>/', ActivateView.as_view(), name='activate'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
