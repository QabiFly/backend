from rest_framework import serializers
from .models import WeatherData, FarmerFieldReport


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = [
            'id', 'node_id', 'location_name', 'temperature', 
            'humidity', 'pressure', 'rainfall', 'soil_moisture',
            'wind_speed', 'rain_probability', 'latitude', 'longitude',
            'alert_level', 'forecast_24h', 'forecast_48h', 
            'forecast_72h', 'crop_advice', 'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at']


class FarmerFieldReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerFieldReport
        fields = [
            'id', 'user', 'crop_type', 'crop_condition',
            'pest_observed', 'irrigation_needed', 'notes',
            'latitude', 'longitude', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
