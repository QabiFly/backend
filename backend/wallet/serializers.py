from rest_framework import serializers
from .models import Wallet, WalletTransaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'id', 'user', 'balance', 'pending_balance', 
            'available_balance', 'total_earned', 'total_withdrawn',
            'upi_id', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = [
            'id', 'wallet', 'amount', 'transaction_type', 
            'purpose', 'order', 'balance_after', 'description',
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
