import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from saleor.account.models import User
from saleor.channel.models import Channel
from saleor.order.models import Order


class Udhaar(models.Model):
    """Digital Khata (Credit) System for QabiFly"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='udhaar_records')
    shop = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='shop_udhaar_records')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='udhaar_records')
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    paid_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    remaining = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    due_date = models.DateTimeField(null=True, blank=True)
    is_overdue = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['shop', 'status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"Udhaar {self.id} - {self.user.email} - ₹{self.amount}"
    
    def save(self, *args, **kwargs):
        # Calculate remaining amount
        self.remaining = self.amount - self.paid_amount
        
        # Check if overdue
        if self.due_date and timezone.now() > self.due_date and self.remaining > 0:
            self.is_overdue = True
            if self.status == 'pending':
                self.status = 'overdue'
        else:
            self.is_overdue = False
            
        super().save(*args, **kwargs)


class SundayCollection(models.Model):
    """Sunday Collection System for Udhaar Payments"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('collected', 'Collected'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_boy = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sunday_collections',
        limit_choices_to={'is_staff': True}
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='my_sunday_collections'
    )
    udhaar = models.ForeignKey(
        Udhaar, 
        on_delete=models.CASCADE, 
        related_name='sunday_collections'
    )
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    collected_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    collection_date = models.DateField()
    collected_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-collection_date']
        indexes = [
            models.Index(fields=['delivery_boy', 'status']),
            models.Index(fields=['user', 'collection_date']),
            models.Index(fields=['collection_date']),
        ]
    
    def __str__(self):
        return f"Sunday Collection {self.id} - {self.user.email} - ₹{self.amount}"
