import uuid
from decimal import Decimal

from django.db import models
from django.utils import timezone

from saleor.account.models import User


class Notification(models.Model):
    """Saleor Notification System"""
    
    NOTIFICATION_TYPES = [
        ('order', 'Order'),
        ('payment', 'Payment'),
        ('delivery', 'Delivery'),
        ('weather', 'Weather'),
        ('promo', 'Promotion'),
        ('udhaar', 'Udhaar'),
        ('system', 'System'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES,
        default='normal'
    )
    
    data = models.JSONField(null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'notification_type']),
            models.Index(fields=['user', 'priority']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Notification - {self.user.email} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    @property
    def is_unread(self):
        """Check if notification is unread"""
        return not self.is_read
