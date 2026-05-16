import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from saleor.account.models import User
from saleor.order.models import Order


class EMI(models.Model):
    """EMI System for Saleor"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('defaulted', 'Defaulted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='emi_plans'
    )
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='emi_plans'
    )
    
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('500.00'))]
    )
    emi_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    months = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(36)]
    )
    interest_rate = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(50.0)]
    )
    
    paid_months = models.PositiveIntegerField(default=0)
    paid_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    remaining_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='active'
    )
    next_due_date = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['next_due_date']),
        ]
    
    def __str__(self):
        return f"EMI - {self.user.email} - ₹{self.total_amount}"
    
    def save(self, *args, **kwargs):
        # Calculate remaining amount
        self.remaining_amount = self.total_amount - self.paid_amount
        
        # Check if completed
        if self.paid_months >= self.months or self.remaining_amount <= 0:
            self.status = 'completed'
            self.paid_months = self.months
            self.remaining_amount = Decimal('0.00')
            
        super().save(*args, **kwargs)


class EMIPayment(models.Model):
    """EMI Payment Records"""
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('wallet', 'Wallet'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emi = models.ForeignKey(
        EMI, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    
    month_number = models.PositiveIntegerField()
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHODS
    )
    
    paid_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-paid_at']
        indexes = [
            models.Index(fields=['emi', 'month_number']),
            models.Index(fields=['emi', 'paid_at']),
            models.Index(fields=['payment_method']),
        ]
    
    def __str__(self):
        return f"EMI Payment - Month {self.month_number} - ₹{self.amount}"
