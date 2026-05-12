from django.contrib import admin

from .models import DeliveryBoy, DeliveryAssignment, DeliveryLocation


@admin.register(DeliveryBoy)
class DeliveryBoyAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'is_available', 'is_online', 
        'total_deliveries', 'rating', 'zone', 'vehicle_type'
    ]
    list_filter = ['is_available', 'is_online', 'vehicle_type', 'zone']
    search_fields = ['user__email', 'zone']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Profile Info', {
            'fields': ('user', 'zone', 'vehicle_type')
        }),
        ('Status', {
            'fields': ('is_available', 'is_online')
        }),
        ('Location', {
            'fields': ('current_latitude', 'current_longitude')
        }),
        ('Performance', {
            'fields': ('total_deliveries', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeliveryAssignment)
class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'order', 'delivery_boy', 'status', 
        'delivery_otp', 'assigned_at', 'delivered_at'
    ]
    list_filter = ['status', 'assigned_at', 'delivered_at']
    search_fields = [
        'order__id', 'delivery_boy__email', 'delivery_otp'
    ]
    readonly_fields = ['id', 'assigned_at', 'accepted_at', 'delivered_at']
    date_hierarchy = 'assigned_at'
    
    fieldsets = (
        ('Assignment Info', {
            'fields': ('order', 'delivery_boy')
        }),
        ('Status', {
            'fields': ('status', 'delivery_otp', 'otp_verified')
        }),
        ('Timestamps', {
            'fields': ('assigned_at', 'accepted_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'delivery_boy', 'order', 'latitude', 
        'longitude', 'speed', 'battery_level', 'recorded_at'
    ]
    list_filter = ['recorded_at']
    search_fields = ['delivery_boy__email', 'order__id']
    readonly_fields = ['id', 'recorded_at']
    date_hierarchy = 'recorded_at'
    
    fieldsets = (
        ('Location Info', {
            'fields': ('delivery_boy', 'order', 'latitude', 'longitude')
        }),
        ('Device Info', {
            'fields': ('speed', 'battery_level')
        }),
        ('Timestamps', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        }),
    )
