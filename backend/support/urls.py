from django.urls import path

from . import views

app_name = "support"

urlpatterns = [
    path('sessions/', views.ChatSessionListView.as_view(), name='chat-session-list'),
    path('sessions/create/', views.ChatSessionCreateView.as_view(), name='chat-session-create'),
    path('sessions/<uuid:pk>/', views.ChatSessionDetailView.as_view(), name='chat-session-detail'),
    path('sessions/<uuid:pk>/messages/', views.ChatMessageListView.as_view(), name='chat-message-list'),
    path('sessions/<uuid:pk>/send/', views.ChatMessageSendView.as_view(), name='chat-message-send'),
]
