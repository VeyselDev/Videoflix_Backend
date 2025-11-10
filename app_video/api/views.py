import os

from django.http import Http404, FileResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app_video.api.serializers import VideoListSerializer
from app_video.models import Video


class VideoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        videos = Video.objects.all().order_by('-created_at')
        serializer = VideoListSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class HLSManifestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        base, _ = os.path.splitext(video.video_file.path)

        playlist_path = os.path.join(f"{base}_{resolution}", "index.m3u8")

        if not os.path.exists(playlist_path):
            raise Http404("Manifest not found")

        return FileResponse(open(playlist_path, 'rb'), content_type='application/vnd.apple.mpegurl')


class HLSSegmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        base, _ = os.path.splitext(video.video_file.path)

        segment_path = os.path.join(f"{base}_{resolution}", segment)

        if not os.path.exists(segment_path):
            raise Http404("Segment not found")

        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')
