from rest_framework import serializers
from .models import KYC


class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = [
            'id', 'user', 'pan_number', 'pan_verified', 
            'pan_document', 'aadhaar_number', 'aadhaar_verified',
            'aadhaar_document', 'bank_name', 'account_number',
            'ifsc_code', 'upi_id', 'bank_verified',
            'status', 'verified_by', 'verified_at', 
            'rejection_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'verified_at']
