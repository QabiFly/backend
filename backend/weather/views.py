from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import WeatherData, FarmerFieldReport
from .serializers import WeatherDataSerializer, FarmerFieldReportSerializer


class WeatherDataListView(ListCreateAPIView):
    """Get all weather data"""
    serializer_class = WeatherDataSerializer
    
    def get_queryset(self):
        return WeatherData.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()


class WeatherDataCreateView(APIView):
    """Create weather data from IoT sensor"""
    
    def post(self, request):
        serializer = WeatherDataSerializer(data=request.data)
        if serializer.is_valid():
            weather_data = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Weather data recorded successfully',
                'weather_data_id': str(weather_data.id)
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class WeatherDataDetailView(APIView):
    """Get specific weather data"""
    
    def get(self, request, pk):
        weather_data = get_object_or_404(WeatherData, id=pk)
        serializer = WeatherDataSerializer(weather_data)
        return Response({
            'status': 'success',
            'weather_data': serializer.data
        })


class FarmerFieldReportListView(ListCreateAPIView):
    """Get all farmer field reports"""
    serializer_class = FarmerFieldReportSerializer
    
    def get_queryset(self):
        return FarmerFieldReport.objects.all()
    
    def perform_create(self, Serializer):
        serializer.save(user=self.request.user)


class FarmerFieldReportCreateView(APIView):
    """Create farmer field report"""
    
    def post(self, request):
        serializer = FarmerFieldReportSerializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save(user=self.request.user)
            return Response({
                'status': 'success',
                'message': 'Field report created successfully',
                'report_id': str(report.id)
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CurrentWeatherView(APIView):
    """Get current weather for Reoti"""
    
    def get(self, request):
        # Get latest weather data for Reoti
        weather = WeatherData.objects.filter(
            location_name__icontains='Reoti'
        ).order_by('-recorded_at').first()
        
        if weather:
            serializer = WeatherDataSerializer(weather)
            return Response({
                'status': 'success',
                'current_weather': serializer.data
            })
        
        return Response({
            'status': 'error',
            'message': 'No weather data available for Reoti'
        }, status=status.HTTP_404_NOT_FOUND)


class WeatherForecastView(APIView):
    """Get weather forecast"""
    
    def get(self, request):
        # Get latest weather data with forecast
        weather = WeatherData.objects.filter(
            forecast_24h__isnull=False
        ).order_by('-recorded_at').first()
        
        if weather and weather.forecast_24h:
            return Response({
                'status': 'success',
                'forecast': weather.forecast_24h
            })
        
        return Response({
            'status': 'error',
            'message': 'No forecast data available'
        }, status=status.HTTP_404_NOT_FOUND)


class CropAdviceView(APIView):
    """Get crop advice from weather data"""
    
    def get(self, request):
        # Get latest weather data with crop advice
        weather = WeatherData.objects.filter(
            crop_advice__isnull=False
        ).order_by('-recorded_at').first()
        
        if weather and weather.crop_advice:
            return Response({
                'status': 'success',
                'crop_advice': weather.crop_advice
            })
        
        return Response({
            'status': 'error',
            'message': 'No crop advice available'
        }, status=status.HTTP_404_NOT_FOUND)
