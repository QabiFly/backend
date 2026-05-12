from django.contrib import admin

from .models import KYC


@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'status', 'pan_verified', 
        'aadhaar_verified', 'bank_verified', 'created_at'
    ]
    list_filter = [
        'status', 'pan_verified', 'aadhaar_verified', 
        'bank_verified', 'created_at'
    ]
    search_fields = [
        'user__email', 'pan_number', 'aadhaar_number',
        'bank_name', 'ifsc_code', 'upi_id'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'verified_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('PAN Card', {
            'fields': ('pan_number', 'pan_verified', 'pan_document')
        }),
        ('Aadhaar Card', {
            'fields': ('aadhaar_number', 'aadhaar_verified', 'aadhaar_document')
        }),
        ('Bank Details', {
            'fields': (
                'bank_name', 'account_number', 'ifsc_code', 
                'upi_id', 'bank_verified'
            )
        }),
        ('Verification', {
            'fields': (
                'status', 'verified_by', 'verified_at', 
                'rejection_reason'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_kyc', 'reject_kyc']
    
    def approve_kyc(self, request, queryset):
        """Approve selected KYC applications"""
        count = 0
        for kyc in queryset:
            if kyc.status in ['pending', 'under_review']:
                kyc.approve(verified_by=request.user)
                count += 1
        self.message_user(request, f'{count} KYC applications approved.')
    approve_kyc.short_description = 'Approve selected KYC'
    
    def reject_kyc(self, request, queryset):
        """Reject selected KYC applications"""
        count = 0
        for kyc in queryset:
            if kyc.status in ['pending', 'under_review']:
                kyc.reject(reason="Rejected by admin", verified_by=request.user)
                count += 1
        self.message_user(request, f'{count} KYC applications rejected.')
    reject_kyc.short_description = 'Reject selected KYC'
