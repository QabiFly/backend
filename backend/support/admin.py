from django.contrib import admin

from .models import ChatSession, ChatMessage


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'channel', 'status', 
        'is_ai', 'assigned_agent', 'created_at'
    ]
    list_filter = [
        'channel', 'status', 'is_ai', 'created_at'
    ]
    search_fields = [
        'user__email', 'assigned_agent__email'
    ]
    readonly_fields = [
        'id', 'created_at', 'resolved_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Session Info', {
            'fields': ('user', 'channel', 'is_ai')
        }),
        ('Status', {
            'fields': ('status', 'assigned_agent', 'user_rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'session', 'sender_type', 'sender', 
        'message_type', 'is_read', 'created_at'
    ]
    list_filter = [
        'sender_type', 'message_type', 'is_read', 'created_at'
    ]
    search_fields = [
        'session__user__email', 'sender__email', 'message'
    ]
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Info', {
            'fields': ('session', 'sender_type', 'sender')
        }),
        ('Content', {
            'fields': ('message', 'message_type')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
