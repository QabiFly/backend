import uuid
from decimal import Decimal

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class GISLandmark(models.Model):
    """Saleor GIS Landmarks"""
    
    LANDMARK_TYPES = [
        ('shop', 'Shop'),
        ('road', 'Road'),
        ('farm', 'Farm'),
        ('water', 'Water'),
        ('hospital', 'Hospital'),
        ('school', 'School'),
        ('market', 'Market'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=200)
    landmark_type = models.CharField(
        max_length=20, 
        choices=LANDMARK_TYPES
    )
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['landmark_type', 'is_active']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.landmark_type.title()} - {self.name}"


class WeatherZone(models.Model):
    """Saleor Weather Zones"""
    
    RISK_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('danger', 'Danger'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    boundary = models.JSONField(
        help_text="Polygon coordinates for zone boundary"
    )
    color = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#[0-9A-Fa-f]{6}$',
                message='Enter a valid hex color code.'
            )
        ],
        help_text="Hex color code for map display"
    )
    
    risk_level = models.CharField(
        max_length=10, 
        choices=RISK_CHOICES,
        default='low'
    )
    description = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['risk_level']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"Weather Zone - {self.name} ({self.risk_level})"
