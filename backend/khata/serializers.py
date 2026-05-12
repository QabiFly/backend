from rest_framework import serializers
from .models import Udhaar, SundayCollection


class UdhaarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Udhaar
        fields = [
            'id', 'user', 'shop', 'order', 'amount', 
            'paid_amount', 'remaining', 'due_date', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SundayCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SundayCollection
        fields = [
            'id', 'delivery_boy', 'user', 'udhaar', 'amount',
            'collected_amount', 'status', 'collection_date',
            'collected_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
