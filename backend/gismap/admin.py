from django.contrib import admin

from .models import GISLandmark, WeatherZone


@admin.register(GISLandmark)
class GISLandmarkAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'landmark_type', 'latitude',
        'longitude', 'is_active', 'created_at'
    ]
    list_filter = [
        'landmark_type', 'is_active', 'created_at'
    ]
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Landmark Info', {
            'fields': ('name', 'landmark_type', 'description')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_landmarks', 'deactivate_landmarks']
    
    def activate_landmarks(self, request, queryset):
        """Activate selected landmarks"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} landmarks activated.')
    activate_landmarks.short_description = 'Activate selected landmarks'
    
    def deactivate_landmarks(self, request, queryset):
        """Deactivate selected landmarks"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} landmarks deactivated.')
    deactivate_landmarks.short_description = 'Deactivate selected landmarks'


@admin.register(WeatherZone)
class WeatherZoneAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'risk_level', 'color',
        'created_at'
    ]
    list_filter = [
        'risk_level', 'created_at'
    ]
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Zone Info', {
            'fields': ('name', 'description', 'risk_level')
        }),
        ('Display', {
            'fields': ('color', 'boundary')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
