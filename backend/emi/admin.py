from django.contrib import admin

from .models import EMI, EMIPayment


@admin.register(EMI)
class EMIAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'order', 'total_amount', 'emi_amount',
        'months', 'paid_months', 'status', 'next_due_date'
    ]
    list_filter = [
        'status', 'created_at', 'next_due_date'
    ]
    search_fields = [
        'user__email', 'order__id'
    ]
    readonly_fields = [
        'id', 'paid_amount', 'remaining_amount', 
        'created_at', 'updated_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('EMI Info', {
            'fields': ('user', 'order', 'total_amount')
        }),
        ('Payment Details', {
            'fields': (
                'emi_amount', 'months', 'interest_rate',
                'paid_months', 'paid_amount', 'remaining_amount'
            )
        }),
        ('Status', {
            'fields': ('status', 'next_due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EMIPayment)
class EMIPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'emi', 'month_number', 'amount',
        'payment_method', 'paid_at'
    ]
    list_filter = [
        'payment_method', 'paid_at'
    ]
    search_fields = [
        'emi__user__email', 'emi__order__id'
    ]
    readonly_fields = ['id', 'paid_at']
    date_hierarchy = 'paid_at'
    
    fieldsets = (
        ('Payment Info', {
            'fields': ('emi', 'month_number', 'amount')
        }),
        ('Payment Method', {
            'fields': ('payment_method',)
        }),
        ('Timestamps', {
            'fields': ('paid_at',),
            'classes': ('collapse',)
        }),
    )
