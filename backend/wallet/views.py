from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import Wallet, WalletTransaction
from .serializers import WalletSerializer, WalletTransactionSerializer


class WalletDetailView(APIView):
    """Get wallet details for authenticated user"""
    
    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        
        return Response({
            'status': 'success',
            'wallet': serializer.data
        })


class WalletTopupView(APIView):
    """Top-up wallet"""
    
    def post(self, request):
        wallet = get_object_or_404(Wallet, user=request.user)
        amount = Decimal(request.data.get('amount', '0'))
        method = request.data.get('method', 'wallet')
        
        if amount <= 0:
            return Response({
                'status': 'error',
                'message': 'Amount must be greater than 0'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create transaction
        transaction = WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='topup',
            purpose=f'Top-up via {method}',
            balance_after=wallet.balance + amount,
            description=f'Wallet top-up of ₹{amount}'
        )
        
        # Update wallet balance
        wallet.balance += amount
        wallet.total_earned += amount
        wallet.save()
        
        return Response({
            'status': 'success',
            'message': f'Wallet topped up successfully with ₹{amount}',
            'new_balance': float(wallet.balance)
        })


class WalletWithdrawView(APIView):
    """Withdraw from wallet"""
    
    def post(self, request):
        wallet = get_object_or_404(Wallet, user=request.user)
        amount = Decimal(request.data.get('amount', '0'))
        upi_id = request.data.get('upi_id', '')
        
        if amount <= 0:
            return Response({
                'status': 'error',
                'message': 'Amount must be greater than 0'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if amount > wallet.available_balance:
            return Response({
                'status': 'error',
                'message': 'Insufficient balance'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create transaction
        transaction = WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='withdrawal',
            purpose=f'Withdrawal to UPI {upi_id}',
            balance_after=wallet.balance - amount,
            description=f'Withdrawal of ₹{amount} to UPI {upi_id}'
        )
        
        # Update wallet
        wallet.balance -= amount
        wallet.total_withdrawn += amount
        wallet.save()
        
        return Response({
            'status': 'success',
            'message': f'Withdrawal of ₹{amount} processed successfully',
            'new_balance': float(wallet.balance)
        })


class WalletTransferView(APIView):
    """Transfer to another user"""
    
    def post(self, request):
        from_wallet = get_object_or_404(Wallet, user=request.user)
        to_user_id = request.data.get('to_user_id')
        amount = Decimal(request.data.get('amount', '0'))
        
        if amount <= 0:
            return Response({
                'status': 'error',
                'message': 'Amount must be greater than 0'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if amount > from_wallet.available_balance:
            return Response({
                'status': 'error',
                'message': 'Insufficient balance'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create transaction for sender
        WalletTransaction.objects.create(
            wallet=from_wallet,
            amount=amount,
            transaction_type='transfer',
            purpose=f'Transfer to user {to_user_id}',
            balance_after=from_wallet.balance - amount,
            description=f'Transfer of ₹{amount} to user {to_user_id}'
        )
        
        # Update sender wallet
        from_wallet.balance -= amount
        from_wallet.save()
        
        # Create transaction for receiver and update their wallet
        to_wallet, created = Wallet.objects.get_or_create(user_id=to_user_id)
        WalletTransaction.objects.create(
            wallet=to_wallet,
            amount=amount,
            transaction_type='transfer',
            purpose=f'Transfer from user {request.user.id}',
            balance_after=to_wallet.balance + amount,
            description=f'Transfer of ₹{amount} from user {request.user.id}'
        )
        to_wallet.balance += amount
        to_wallet.total_earned += amount
        to_wallet.save()
        
        return Response({
            'status': 'success',
            'message': f'Transfer of ₹{amount} processed successfully',
            'new_balance': float(from_wallet.balance)
        })


class WalletTransactionListView(ListCreateAPIView):
    """Get wallet transactions for authenticated user"""
    serializer_class = WalletTransactionSerializer
    
    def get_queryset(self):
        wallet = Wallet.objects.get_or_create(user=self.request.user)
        return WalletTransaction.objects.filter(wallet=wallet)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
