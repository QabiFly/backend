from django.contrib import admin

from .models import VideoContent


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'category', 'duration_seconds',
        'view_count', 'is_active', 'created_at'
    ]
    list_filter = [
        'category', 'is_active', 'created_at'
    ]
    search_fields = [
        'title', 'description', 'youtube_id'
    ]
    readonly_fields = [
        'id', 'view_count', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Video Info', {
            'fields': ('title', 'description', 'category')
        }),
        ('YouTube Details', {
            'fields': ('youtube_url', 'youtube_id', 'thumbnail_url')
        }),
        ('Video Details', {
            'fields': ('duration_seconds', 'is_active', 'view_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_videos', 'deactivate_videos']
    
    def activate_videos(self, request, queryset):
        """Activate selected videos"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} videos activated.')
    activate_videos.short_description = 'Activate selected videos'
    
    def deactivate_videos(self, request, queryset):
        """Deactivate selected videos"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} videos deactivated.')
    deactivate_videos.short_description = 'Deactivate selected videos'
