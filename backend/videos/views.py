from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import VideoContent
from .serializers import VideoContentSerializer


class VideoContentListView(ListCreateAPIView):
    """Get all video content"""
    serializer_class = VideoContentSerializer
    
    def get_queryset(self):
        return VideoContent.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        serializer.save()


class VideoContentCreateView(APIView):
    """Create new video content"""
    
    def post(self, request):
        serializer = VideoContentSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            return Response({
                'status': 'success',
                'video_id': str(video.id),
                'message': 'Video content created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class VideoContentDetailView(APIView):
    """Get video content details"""
    
    def get(self, request, pk):
        video = get_object_or_404(VideoContent, id=pk)
        serializer = VideoContentSerializer(video)
        
        return Response({
            'status': 'success',
            'video': serializer.data
        })


class VideoContentViewIncrementView(APIView):
    """Increment video view count"""
    
    def post(self, request, pk):
        try:
            video = get_object_or_404(VideoContent, id=pk)
            video.increment_view_count()
            
            return Response({
                'status': 'success',
                'message': 'View count incremented successfully',
                'view_count': video.view_count
            })
            
        except VideoContent.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Video not found'
            }, status=status.HTTP_404_NOT_FOUND)
