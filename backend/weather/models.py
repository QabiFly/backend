import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from saleor.account.models import User


class WeatherData(models.Model):
    """IoT Weather Data from ESP32 Sensors"""
    
    ALERT_CHOICES = [
        ('normal', 'Normal'),
        ('watch', 'Watch'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    node_id = models.CharField(
        max_length=50,
        help_text="ESP32 sensor identifier"
    )
    
    # Sensor readings
    temperature = models.FloatField(
        help_text="Temperature in Celsius",
        validators=[MinValueValidator(-50.0), MaxValueValidator(60.0)]
    )
    humidity = models.FloatField(
        help_text="Humidity percentage",
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    pressure = models.FloatField(
        help_text="Atmospheric pressure in hPa",
        validators=[MinValueValidator(800.0), MaxValueValidator(1200.0)]
    )
    rainfall = models.FloatField(
        help_text="Rainfall in mm",
        validators=[MinValueValidator(0.0)]
    )
    soil_moisture = models.FloatField(
        help_text="Soil moisture percentage",
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    wind_speed = models.FloatField(
        help_text="Wind speed in km/h",
        validators=[MinValueValidator(0.0)]
    )
    rain_probability = models.FloatField(
        help_text="Rain probability percentage",
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    
    # Location
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        help_text="GPS latitude"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        help_text="GPS longitude"
    )
    location_name = models.CharField(
        max_length=100,
        help_text="Human readable location name"
    )
    
    # Forecasts and advice
    forecast_24h = models.JSONField(null=True, blank=True)
    forecast_48h = models.JSONField(null=True, blank=True)
    forecast_72h = models.JSONField(null=True, blank=True)
    crop_advice = models.JSONField(null=True, blank=True)
    
    alert_level = models.CharField(
        max_length=10, 
        choices=ALERT_CHOICES,
        default='normal'
    )
    
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['node_id', 'recorded_at']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['alert_level']),
            models.Index(fields=['recorded_at']),
        ]
    
    def __str__(self):
        return f"Weather Data - {self.location_name} at {self.recorded_at}"


class FarmerFieldReport(models.Model):
    """Farmer Field Reports"""
    
    CROP_CONDITION_CHOICES = [
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='field_reports'
    )
    
    crop_type = models.CharField(max_length=100)
    crop_condition = models.CharField(
        max_length=10, 
        choices=CROP_CONDITION_CHOICES
    )
    pest_observed = models.BooleanField(default=False)
    irrigation_needed = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['crop_type']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Field Report - {self.user.email} - {self.crop_type}"
