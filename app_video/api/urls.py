from django.urls import path
from .views import VideoListView, VideoPlaylistView, VideoSegmentView

urlpatterns = [
    path('api/video/', VideoListView.as_view(), name='video_list'),
    path('api/video/<int:movie_id>/<str:resolution>/index.m3u8', VideoPlaylistView.as_view(), name='video_playlist'),
    path('api/video/<int:movie_id>/<str:resolution>/<str:segment>/', VideoSegmentView.as_view(), name='video_segment'),
]
