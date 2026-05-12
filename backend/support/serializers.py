from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = [
            'id', 'user', 'channel', 'status', 'is_ai',
            'assigned_agent', 'user_rating', 'created_at',
            'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'resolved_at']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'session', 'sender_type', 'sender',
            'message', 'message_type', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
