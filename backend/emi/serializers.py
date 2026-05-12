from rest_framework import serializers
from .models import EMI, EMIPayment


class EMISerializer(serializers.ModelSerializer):
    class Meta:
        model = EMI
        fields = [
            'id', 'user', 'order', 'total_amount', 'emi_amount',
            'months', 'interest_rate', 'paid_months', 'paid_amount',
            'remaining_amount', 'status', 'next_due_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EMIPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EMIPayment
        fields = [
            'id', 'emi', 'month_number', 'amount',
            'payment_method', 'paid_at'
        ]
        read_only_fields = ['id', 'paid_at']
