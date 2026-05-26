from django.urls import path
from .views import VideoListView, HLSManifestView, HLSSegmentView


"""
URL routing for video-related endpoints.

Includes:
- Video listing endpoint
- HLS streaming manifest endpoint
- HLS segment serving endpoint
"""


urlpatterns = [
    path('video/', VideoListView.as_view(), name='video_list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', HLSManifestView.as_view(), name='hls_manifest'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', HLSSegmentView.as_view(), name='hls_segment'),
]