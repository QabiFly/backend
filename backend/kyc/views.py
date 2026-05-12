from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import KYC
from .serializers import KYCSerializer


class KYCDetailView(APIView):
    """Get KYC details for authenticated user"""
    
    def get(self, request):
        kyc, created = KYC.objects.get_or_create(user=request.user)
        serializer = KYCSerializer(kyc)
        
        return Response({
            'status': 'success',
            'kyc': serializer.data
        })


class KYCUploadView(APIView):
    """Upload KYC documents"""
    
    def post(self, request):
        kyc, created = KYC.objects.get_or_create(user=request.user)
        serializer = KYCSerializer(kyc, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'KYC documents uploaded successfully',
                'kyc': serializer.data
            })
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class KYCAdminListView(ListCreateAPIView):
    """Get all KYC applications for admin"""
    serializer_class = KYCSerializer
    
    def get_queryset(self):
        return KYC.objects.all()


class KYCApproveView(APIView):
    """Approve KYC application"""
    
    def post(self, request, pk):
        try:
            kyc = get_object_or_404(KYC, id=pk)
            kyc.approve(verified_by=request.user)
            
            return Response({
                'status': 'success',
                'message': 'KYC approved successfully'
            })
            
        except KYC.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'KYC not found'
            }, status=status.HTTP_404_NOT_FOUND)


class KYCRejectView(APIView):
    """Reject KYC application"""
    
    def post(self, request, pk):
        try:
            kyc = get_object_or_404(KYC, id=pk)
            reason = request.data.get('rejection_reason', '')
            kyc.reject(reason=reason, verified_by=request.user)
            
            return Response({
                'status': 'success',
                'message': 'KYC rejected successfully'
            })
            
        except KYC.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'KYC not found'
            }, status=status.HTTP_404_NOT_FOUND)
