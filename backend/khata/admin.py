from django.contrib import admin

from .models import Udhaar, SundayCollection


@admin.register(Udhaar)
class UdhaarAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'shop', 'amount', 'paid_amount', 
        'remaining', 'status', 'due_date', 'created_at'
    ]
    list_filter = ['status', 'is_overdue', 'created_at', 'due_date']
    search_fields = ['user__email', 'shop__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'remaining']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'shop', 'order')
        }),
        ('Amount Details', {
            'fields': ('amount', 'paid_amount', 'remaining')
        }),
        ('Status', {
            'fields': ('status', 'due_date', 'is_overdue')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SundayCollection)
class SundayCollectionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'delivery_boy', 'user', 'udhaar', 
        'amount', 'collected_amount', 'status', 'collection_date'
    ]
    list_filter = ['status', 'collection_date', 'created_at']
    search_fields = [
        'delivery_boy__email', 'user__email', 
        'udhaar__id', 'notes'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'collection_date'
    
    fieldsets = (
        ('Collection Info', {
            'fields': ('delivery_boy', 'user', 'udhaar')
        }),
        ('Amount Details', {
            'fields': ('amount', 'collected_amount')
        }),
        ('Status', {
            'fields': ('status', 'collection_date', 'collected_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
