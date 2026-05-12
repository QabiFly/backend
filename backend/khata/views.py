from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import Udhaar, SundayCollection
from .serializers import UdhaarSerializer, SundayCollectionSerializer


class UdhaarListView(ListCreateAPIView):
    """Get all Udhaar records for a user"""
    serializer_class = UdhaarSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Udhaar.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UdhaarCreateView(APIView):
    """Create new Udhaar record"""
    
    def post(self, request):
        serializer = UdhaarSerializer(data=request.data)
        if serializer.is_valid():
            udhaar = serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'udhaar_id': str(udhaar.id),
                'message': 'Udhaar created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UdhaarPayView(APIView):
    """Pay Udhaar amount"""
    
    def post(self, request, pk):
        try:
            udhaar = get_object_or_404(Udhaar, id=pk, user=request.user)
            amount = Decimal(request.data.get('amount', '0'))
            
            if amount <= 0:
                return Response({
                    'status': 'error',
                    'message': 'Amount must be greater than 0'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if amount > udhaar.remaining:
                return Response({
                    'status': 'error',
                    'message': 'Amount exceeds remaining balance'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update udhaar
            udhaar.paid_amount += amount
            udhaar.save()
            
            return Response({
                'status': 'success',
                'message': f'Payment of ₹{amount} recorded successfully',
                'remaining': float(udhaar.remaining)
            })
            
        except Udhaar.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Udhaar not found'
            }, status=status.HTTP_404_NOT_FOUND)


class SundayCollectionView(ListCreateAPIView):
    """Get all Sunday collections for delivery boy"""
    serializer_class = SundayCollectionSerializer
    
    def get_queryset(self):
        user = self.request.user
        return SundayCollection.objects.filter(delivery_boy=user)


class SundayCollectionCreateView(APIView):
    """Create new Sunday collection"""
    
    def post(self, request):
        serializer = SundayCollectionSerializer(data=request.data)
        if serializer.is_valid():
            collection = serializer.save(delivery_boy=request.user)
            return Response({
                'status': 'success',
                'collection_id': str(collection.id),
                'message': 'Sunday collection created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SundayCollectionCollectView(APIView):
    """Collect Sunday collection amount"""
    
    def post(self, request, pk):
        try:
            collection = get_object_or_404(SundayCollection, id=pk, delivery_boy=request.user)
            amount = Decimal(request.data.get('collected_amount', '0'))
            
            if amount <= 0:
                return Response({
                    'status': 'error',
                    'message': 'Amount must be greater than 0'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update collection
            collection.collected_amount = amount
            collection.status = 'collected'
            collection.collected_at = timezone.now()
            collection.save()
            
            # Update udhaar
            if collection.udhaar:
                collection.udhaar.paid_amount += amount
                collection.udhaar.save()
            
            return Response({
                'status': 'success',
                'message': f'Collection of ₹{amount} recorded successfully',
                'udhaar_remaining': float(collection.udhaar.remaining) if collection.udhaar else None
            })
            
        except SundayCollection.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Collection not found'
            }, status=status.HTTP_404_NOT_FOUND)
