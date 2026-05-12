from rest_framework import serializers
from .models import VideoContent


class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = [
            'id', 'title', 'description', 'category',
            'youtube_url', 'youtube_id', 'thumbnail_url',
            'duration_seconds', 'is_active', 'view_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
