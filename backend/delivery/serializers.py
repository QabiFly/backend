from rest_framework import serializers
from .models import DeliveryBoy, DeliveryAssignment, DeliveryLocation


class DeliveryBoySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryBoy
        fields = [
            'id', 'user', 'is_available', 'is_online',
            'current_latitude', 'current_longitude', 'total_deliveries',
            'rating', 'zone', 'vehicle_type', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAssignment
        fields = [
            'id', 'order', 'delivery_boy', 'status', 
            'delivery_otp', 'otp_verified', 'assigned_at',
            'accepted_at', 'delivered_at'
        ]
        read_only_fields = ['id', 'assigned_at', 'accepted_at', 'delivered_at']


class DeliveryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocation
        fields = [
            'id', 'delivery_boy', 'order', 'latitude', 
            'longitude', 'speed', 'battery_level', 'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at']
