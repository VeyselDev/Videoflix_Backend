from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from core.settings import settings


"""
Main URL configuration for the project.

Routes:
- /admin/          Django admin interface
- /django-rq/      RQ dashboard for background jobs
- /                Health check endpoints
- /api/            Authentication and video APIs
- MEDIA_URL        Static media files (only in DEBUG mode)
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('', include("app_health_check.urls")),
    path('api/', include('app_auth.api.urls')),
    path('api/', include('app_video.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)