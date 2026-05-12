import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

from saleor.account.models import User
from saleor.order.models import Order


class DeliveryBoy(models.Model):
    """Delivery Boy Profile"""
    
    VEHICLE_TYPES = [
        ('bicycle', 'Bicycle'),
        ('motorcycle', 'Motorcycle'),
        ('scooter', 'Scooter'),
        ('auto_rickshaw', 'Auto Rickshaw'),
        ('van', 'Van'),
        ('car', 'Car'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='delivery_profile'
    )
    
    is_available = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    
    current_latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        null=True, 
        blank=True
    )
    current_longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        null=True, 
        blank=True
    )
    
    total_deliveries = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2,
        default=Decimal('5.00'),
        validators=[
            MinValueValidator(Decimal('0.00')),
            MaxValueValidator(Decimal('5.00'))
        ]
    )
    
    zone = models.CharField(max_length=100, blank=True)
    vehicle_type = models.CharField(
        max_length=20, 
        choices=VEHICLE_TYPES,
        default='motorcycle'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['is_available', 'is_online']),
            models.Index(fields=['zone']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"Delivery Boy - {self.user.email} ({self.rating}/5.0)"


class DeliveryAssignment(models.Model):
    """Delivery Assignment Tracking"""
    
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('accepted', 'Accepted'),
        ('picked', 'Picked'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE, 
        related_name='delivery_assignment'
    )
    delivery_boy = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='delivery_assignments',
        limit_choices_to={'is_staff': True}
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='assigned'
    )
    
    delivery_otp = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='OTP must be 6 digits.'
            )
        ]
    )
    otp_verified = models.BooleanField(default=False)
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-assigned_at']
        indexes = [
            models.Index(fields=['delivery_boy', 'status']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_at']),
        ]
    
    def __str__(self):
        return f"Delivery {self.id} - Order {self.order.id} - {self.status}"


class DeliveryLocation(models.Model):
    """Real-time Delivery Location Tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_boy = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='location_updates'
    )
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='location_updates'
    )
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    speed = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.0)]
    )
    battery_level = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['delivery_boy', 'recorded_at']),
            models.Index(fields=['order', 'recorded_at']),
            models.Index(fields=['recorded_at']),
        ]
    
    def __str__(self):
        return f"Location Update - {self.delivery_boy.email} at {self.recorded_at}"
