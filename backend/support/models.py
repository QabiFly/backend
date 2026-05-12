import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from saleor.account.models import User


class ChatSession(models.Model):
    """Chat Support Sessions"""
    
    CHANNEL_CHOICES = [
        ('ai_chat', 'AI Chat'),
        ('phone', 'Phone'),
        ('text', 'Text'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='chat_sessions'
    )
    
    channel = models.CharField(
        max_length=20, 
        choices=CHANNEL_CHOICES,
        default='ai_chat'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    is_ai = models.BooleanField(default=True)
    assigned_agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_chats',
        limit_choices_to={'is_staff': True}
    )
    
    user_rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['assigned_agent', 'status']),
            models.Index(fields=['is_ai', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Chat Session - {self.user.email} - {self.status.title()}"


class ChatMessage(models.Model):
    """Chat Messages"""
    
    SENDER_TYPES = [
        ('user', 'User'),
        ('agent', 'Agent'),
        ('ai', 'AI'),
    ]
    
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    
    sender_type = models.CharField(
        max_length=10, 
        choices=SENDER_TYPES
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_messages'
    )
    
    message = models.TextField()
    message_type = models.CharField(
        max_length=10, 
        choices=MESSAGE_TYPES,
        default='text'
    )
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'sender_type']),
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Message - {self.sender_type} - {self.created_at}"
