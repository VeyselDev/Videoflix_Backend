from rest_framework import serializers
from app_video.models import Video

class VideoListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id',
            'created_at',
            'title',
            'description',
            'thumbnail_url',
            'category',
        ]

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None
