from typing import Any
from django.http import FileResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app_video.api.serializers import VideoListSerializer
from app_video.models.video import Video

from app_video.services.video_service import (
    get_hls_converted_videos,
    get_video_or_404,
    get_hls_file_path_or_404
)


class VideoListView(APIView):
    """
    Returns a list of videos that have been converted to HLS format.

    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        converted_videos: list[Video] = get_hls_converted_videos()
        serializer: VideoListSerializer = VideoListSerializer(
            converted_videos, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class HLSManifestView(APIView):
    """
    Serves the HLS manifest (index.m3u8) file for a given video and resolution.

    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, movie_id: int, resolution: str, *args: Any, **kwargs: Any) -> FileResponse:
        video: Video = get_video_or_404(movie_id)
        manifest_file_path: str = get_hls_file_path_or_404(video, resolution, 'index.m3u8')
        return FileResponse(open(manifest_file_path, 'rb'), content_type='application/vnd.apple.mpegurl')


class HLSSegmentView(APIView):
    """
    Serves individual HLS video segments (.ts files) for streaming.

    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, movie_id: int, resolution: str, segment: str, *args: Any, **kwargs: Any) -> FileResponse:
        video: Video = get_video_or_404(movie_id)
        segment_file_path: str = get_hls_file_path_or_404(video, resolution, segment)
        return FileResponse(open(segment_file_path, 'rb'), content_type='video/MP2T')