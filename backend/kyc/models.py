import uuid
from decimal import Decimal

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from saleor.account.models import User


class KYC(models.Model):
    """Saleor KYC System"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='kyc'
    )
    
    # PAN Card
    pan_number = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
                message='Enter a valid PAN number.'
            )
        ]
    )
    pan_verified = models.BooleanField(default=False)
    pan_document = models.FileField(
        upload_to='kyc/pan/',
        null=True, 
        blank=True
    )
    
    # Aadhaar Card
    aadhaar_number = models.CharField(
        max_length=12,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message='Aadhaar number must be 12 digits.'
            )
        ]
    )
    aadhaar_verified = models.BooleanField(default=False)
    aadhaar_document = models.FileField(
        upload_to='kyc/aadhaar/',
        null=True, 
        blank=True
    )
    
    # Bank Details
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{9,18}$',
                message='Enter a valid bank account number.'
            )
        ]
    )
    ifsc_code = models.CharField(
        max_length=11,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{4}0[A-Z0-9]{6}$',
                message='Enter a valid IFSC code.'
            )
        ]
    )
    upi_id = models.CharField(
        max_length=50,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9.\-+_@]+$',
                message='Enter a valid UPI ID.'
            )
        ]
    )
    bank_verified = models.BooleanField(default=False)
    
    # Verification Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending'
    )
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_kyc',
        limit_choices_to={'is_staff': True}
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['verified_at']),
        ]
    
    def __str__(self):
        return f"KYC - {self.user.email} - {self.status.title()}"
    
    def approve(self, verified_by=None):
        """Approve KYC"""
        self.status = 'verified'
        self.verified_by = verified_by
        self.verified_at = timezone.now()
        self.save()
    
    def reject(self, reason, verified_by=None):
        """Reject KYC"""
        self.status = 'rejected'
        self.rejection_reason = reason
        self.verified_by = verified_by
        self.save()
