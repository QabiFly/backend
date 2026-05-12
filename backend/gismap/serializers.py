from rest_framework import serializers
from .models import GISLandmark, WeatherZone


class GISLandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISLandmark
        fields = [
            'id', 'name', 'landmark_type', 'latitude',
            'longitude', 'description', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WeatherZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherZone
        fields = [
            'id', 'name', 'boundary', 'color',
            'risk_level', 'description', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
