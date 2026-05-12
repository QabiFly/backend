from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import DeliveryBoy, DeliveryAssignment, DeliveryLocation
from .serializers import DeliveryBoySerializer, DeliveryAssignmentSerializer, DeliveryLocationSerializer


class DeliveryBoyListView(ListCreateAPIView):
    """Get all delivery boys"""
    serializer_class = DeliveryBoySerializer
    
    def get_queryset(self):
        return DeliveryBoy.objects.select_related('user').all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeliveryBoyDetailView(APIView):
    """Get delivery boy details"""
    
    def get(self, request, pk):
        delivery_boy = get_object_or_404(DeliveryBoy, id=pk)
        serializer = DeliveryBoySerializer(delivery_boy)
        return Response({
            'status': 'success',
            'delivery_boy': serializer.data
        })


class DeliveryAssignmentListView(ListCreateAPIView):
    """Get all delivery assignments"""
    serializer_class = DeliveryAssignmentSerializer
    
    def get_queryset(self):
        user = self.request.user
        return DeliveryAssignment.objects.filter(delivery_boy=user)
    
    def perform_create(self, serializer):
        serializer.save(delivery_boy=self.request.user)


class DeliveryAssignmentAcceptView(APIView):
    """Accept delivery assignment"""
    
    def post(self, request, pk):
        assignment = get_object_or_404(DeliveryAssignment, id=pk, delivery_boy=request.user)
        
        if assignment.status != 'assigned':
            return Response({
                'status': 'error',
                'message': 'Assignment cannot be accepted'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        assignment.status = 'accepted'
        assignment.accepted_at = timezone.now()
        assignment.save()
        
        return Response({
            'status': 'success',
            'message': 'Assignment accepted successfully'
        })


class DeliveryAssignmentVerifyOTPView(APIView):
    """Verify delivery OTP"""
    
    def post(self, request, pk):
        assignment = get_object_or_404(DeliveryAssignment, id=pk, delivery_boy=request.user)
        provided_otp = request.data.get('otp', '')
        
        if not provided_otp:
            return Response({
                'status': 'error',
                'message': 'OTP is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if provided_otp != assignment.delivery_otp:
            return Response({
                'status': 'error',
                'message': 'Invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        assignment.otp_verified = True
        assignment.save()
        
        return Response({
            'status': 'success',
            'message': 'OTP verified successfully'
        })


class DeliveryLocationListView(ListCreateAPIView):
    """Get delivery locations"""
    serializer_class = DeliveryLocationSerializer
    
    def get_queryset(self):
        user = self.request.user
        return DeliveryLocation.objects.filter(delivery_boy=user)
    
    def perform_create(self, serializer):
        serializer.save(delivery_boy=self.request.user)


class DeliveryLocationUpdateView(APIView):
    """Update delivery boy location"""
    
    def post(self, request):
        serializer = DeliveryLocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(delivery_boy=request.user)
            return Response({
                'status': 'success',
                'message': 'Location updated successfully',
                'location': serializer.data
            })
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
