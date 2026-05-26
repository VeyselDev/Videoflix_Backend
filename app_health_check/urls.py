from django.urls import path

from app_health_check.views import LivenessView

"""
URL configuration for health check endpoints.

Provides a simple liveness endpoint that can be used by load balancers,
monitoring systems, or container orchestration platforms to verify that
the application is running.
"""

urlpatterns = [
    path("health/", LivenessView.as_view(), name="health"),
]