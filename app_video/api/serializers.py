from typing import Optional

from rest_framework import serializers
from rest_framework.request import Request

from app_video.models import Video
from app_video.utils.path_utils import get_file_url


class VideoListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'category', 'thumbnail_url', 'created_at']

    def get_thumbnail_url(self, obj: Video) -> str:
        request: Optional[Request] = self.context.get('request')
        url: str = get_file_url(obj.thumbnail)
        return request.build_absolute_uri(url) if request else url
