import os

import django_rq
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
        all_videos = Video.objects.all().order_by('-created_at')

        job_ids = [v.rq_job_id for v in all_videos if v.rq_job_id]
        if not job_ids:
            serializer = VideoListSerializer([], many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        queue = django_rq.get_queue('default')
        jobs = {job.id: job for job in queue.jobs if job.id in job_ids}

        ready_videos = []
        for video in all_videos:
            job = jobs.get(video.rq_job_id)
            if job is None or job.is_finished:
                ready_videos.append(video)

        serializer = VideoListSerializer(ready_videos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class HLSManifestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        base_dir = os.path.dirname(video.video_file.path)
        playlist_path = os.path.join(base_dir, 'hls', resolution, 'index.m3u8')

        if not os.path.exists(playlist_path):
            raise Http404(f"Manifest not found: {playlist_path}")

        return FileResponse(open(playlist_path, 'rb'), content_type='application/vnd.apple.mpegurl')


class HLSSegmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, segment):
        try:
            video = Video.objects.get(id=movie_id)
        except Video.DoesNotExist:
            raise Http404("Video not found")

        base_dir = os.path.dirname(video.video_file.path)

        segment_path = os.path.join(base_dir, 'hls', resolution, segment)

        if not os.path.exists(segment_path):
            raise Http404(f"Segment not found: {segment_path}")

        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')
