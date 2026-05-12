from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer


class ChatSessionListView(ListCreateAPIView):
    """Get all chat sessions for user"""
    serializer_class = ChatSessionSerializer
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatSessionCreateView(APIView):
    """Create new chat session"""
    
    def post(self, request):
        serializer = ChatSessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save(user=request.user)
            return Response({
                'status': 'success',
                'session_id': str(session.id),
                'message': 'Chat session created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChatSessionDetailView(APIView):
    """Get chat session details"""
    
    def get(self, request, pk):
        session = get_object_or_404(ChatSession, id=pk, user=request.user)
        serializer = ChatSessionSerializer(session)
        
        return Response({
            'status': 'success',
            'session': serializer.data
        })


class ChatMessageListView(ListCreateAPIView):
    """Get all messages in a chat session"""
    serializer_class = ChatMessageSerializer
    
    def get_queryset(self):
        session_id = self.kwargs.get('pk')
        return ChatMessage.objects.filter(session_id=session_id)
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ChatMessageSendView(APIView):
    """Send message in chat session"""
    
    def post(self, request, pk):
        session = get_object_or_404(ChatSession, id=pk, user=request.user)
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(session=session, sender=self.request.user)
            return Response({
                'status': 'success',
                'message_id': str(message.id),
                'message': 'Message sent successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
