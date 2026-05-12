from django.contrib import admin

from .models import Wallet, WalletTransaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'balance', 'pending_balance', 
        'total_earned', 'total_withdrawn', 'upi_id', 'is_active'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__email', 'upi_id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'available_balance']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Wallet Info', {
            'fields': ('user', 'upi_id', 'is_active')
        }),
        ('Balance Details', {
            'fields': ('balance', 'pending_balance', 'available_balance')
        }),
        ('Totals', {
            'fields': ('total_earned', 'total_withdrawn')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'wallet', 'transaction_type', 'amount', 
        'purpose', 'balance_after', 'status', 'created_at'
    ]
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = [
        'wallet__user__email', 'purpose', 'description'
    ]
    readonly_fields = ['id', 'created_at', 'balance_after']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Transaction Info', {
            'fields': ('wallet', 'transaction_type', 'amount')
        }),
        ('Details', {
            'fields': ('purpose', 'order', 'description')
        }),
        ('Status', {
            'fields': ('status', 'balance_after')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
