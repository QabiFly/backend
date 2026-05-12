import uuid
from decimal import Decimal

from django.core.validators import URLValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class VideoContent(models.Model):
    """QabiFly Video Content System"""
    
    CATEGORY_CHOICES = [
        ('farming', 'Farming'),
        ('weather', 'Weather'),
        ('business', 'Business'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('news', 'News'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES
    )
    
    # YouTube Integration
    youtube_url = models.URLField(
        blank=True,
        validators=[URLValidator()]
    )
    youtube_id = models.CharField(
        max_length=20,
        blank=True,
        help_text="YouTube video ID"
    )
    thumbnail_url = models.URLField(
        blank=True,
        validators=[URLValidator()]
    )
    
    # Video Details
    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_active']),
            models.Index(fields=['view_count']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Video - {self.title} ({self.category.title()})"
    
    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
