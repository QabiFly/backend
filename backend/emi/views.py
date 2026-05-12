from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import EMI, EMIPayment
from .serializers import EMISerializer, EMIPaymentSerializer


class EMIListView(ListCreateAPIView):
    """Get all EMI plans for authenticated user"""
    serializer_class = EMISerializer
    
    def get_queryset(self):
        return EMI.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EMICreateView(APIView):
    """Create new EMI plan"""
    
    def post(self, request):
        serializer = EMISerializer(data=request.data)
        if serializer.is_valid():
            emi = serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'emi_id': str(emi.id),
                'message': 'EMI plan created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class EMIDetailView(APIView):
    """Get EMI plan details"""
    
    def get(self, request, pk):
        emi = get_object_or_404(EMI, id=pk, user=request.user)
        serializer = EMISerializer(emi)
        
        return Response({
            'status': 'success',
            'emi': serializer.data
        })


class EMIPayView(APIView):
    """Pay EMI installment"""
    
    def post(self, request, pk):
        try:
            emi = get_object_or_404(EMI, id=pk, user=request.user)
            amount = Decimal(request.data.get('amount', '0'))
            payment_method = request.data.get('payment_method', 'cash')
            
            if amount <= 0:
                return Response({
                    'status': 'error',
                    'message': 'Amount must be greater than 0'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if amount > emi.remaining_amount:
                return Response({
                    'status': 'error',
                    'message': 'Amount exceeds remaining balance'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create EMI payment
            EMIPayment.objects.create(
                emi=emi,
                month_number=emi.paid_months + 1,
                amount=amount,
                payment_method=payment_method
            )
            
            # Update EMI
            emi.paid_months += 1
            emi.paid_amount += amount
            emi.save()
            
            return Response({
                'status': 'success',
                'message': f'EMI payment of ₹{amount} recorded successfully',
                'remaining_amount': float(emi.remaining_amount)
            })
            
        except EMI.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'EMI plan not found'
            }, status=status.HTTP_404_NOT_FOUND)
