from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import GISLandmark, WeatherZone
from .serializers import GISLandmarkSerializer, WeatherZoneSerializer


class GISLandmarkListView(ListCreateAPIView):
    """Get all GIS landmarks"""
    serializer_class = GISLandmarkSerializer
    
    def get_queryset(self):
        return GISLandmark.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        serializer.save()


class GISLandmarkCreateView(APIView):
    """Create new GIS landmark"""
    
    def post(self, request):
        serializer = GISLandmarkSerializer(data=request.data)
        if serializer.is_valid():
            landmark = serializer.save()
            return Response({
                'status': 'success',
                'landmark_id': str(landmark.id),
                'message': 'Landmark created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class GISLandmarkDetailView(APIView):
    """Get GIS landmark details"""
    
    def get(self, request, pk):
        landmark = get_object_or_404(GISLandmark, id=pk)
        serializer = GISLandmarkSerializer(landmark)
        
        return Response({
            'status': 'success',
            'landmark': serializer.data
        })


class WeatherZoneListView(ListCreateAPIView):
    """Get all weather zones"""
    serializer_class = WeatherZoneSerializer
    
    def get_queryset(self):
        return WeatherZone.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()


class WeatherZoneCreateView(APIView):
    """Create new weather zone"""
    
    def post(self, request):
        serializer = WeatherZoneSerializer(data=request.data)
        if serializer.is_valid():
            zone = serializer.save()
            return Response({
                'status': 'success',
                'zone_id': str(zone.id),
                'message': 'Weather zone created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
