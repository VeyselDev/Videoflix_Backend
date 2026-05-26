from typing import Optional

from rest_framework import serializers
from rest_framework.request import Request

from app_video.models.video import Video
from core.utils.path_utils import get_file_url


class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Video objects.

    Provides a computed absolute thumbnail URL when request context is available.
    """
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'category', 'thumbnail_url', 'created_at']

    def get_thumbnail_url(self, obj: Video) -> str:
        """
        Returns the absolute or relative URL of the video thumbnail.

        If the request context exists, the URL is converted to an absolute URL.
        """
        request: Optional[Request] = self.context.get('request')
        url: str = get_file_url(obj.thumbnail)
        return request.build_absolute_uri(url) if request else url