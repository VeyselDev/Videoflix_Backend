from django.urls import path

from app_health_check.views import LivenessView

urlpatterns = [
    path("health/", LivenessView.as_view(), name="health"),
]
