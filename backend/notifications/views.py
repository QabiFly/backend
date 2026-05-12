from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(ListCreateAPIView):
    """Get all notifications for authenticated user"""
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationMarkReadView(APIView):
    """Mark notification as read"""
    
    def post(self, request, pk):
        notification = get_object_or_404(Notification, id=pk, user=request.user)
        notification.mark_as_read()
        
        return Response({
            'status': 'success',
            'message': 'Notification marked as read'
        })


class NotificationMarkAllReadView(APIView):
    """Mark all notifications as read"""
    
    def post(self, request):
        count = request.user.notifications.filter(is_read=False).update(is_read=True)
        
        return Response({
            'status': 'success',
            'message': f'{count} notifications marked as read'
        })
