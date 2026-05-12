from django.contrib import admin

from .models import WeatherData, FarmerFieldReport


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'node_id', 'location_name', 'temperature', 
        'humidity', 'alert_level', 'recorded_at'
    ]
    list_filter = [
        'alert_level', 'node_id', 'location_name', 'recorded_at'
    ]
    search_fields = ['node_id', 'location_name']
    readonly_fields = ['id', 'recorded_at']
    date_hierarchy = 'recorded_at'
    
    fieldsets = (
        ('Sensor Info', {
            'fields': ('node_id', 'location_name')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Weather Readings', {
            'fields': (
                'temperature', 'humidity', 'pressure', 
                'rainfall', 'soil_moisture', 'wind_speed', 
                'rain_probability'
            )
        }),
        ('Forecasts', {
            'fields': ('forecast_24h', 'forecast_48h', 'forecast_72h', 'crop_advice'),
            'classes': ('collapse',)
        }),
        ('Alert Level', {
            'fields': ('alert_level',)
        }),
        ('Timestamps', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FarmerFieldReport)
class FarmerFieldReportAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'crop_type', 'crop_condition', 
        'pest_observed', 'irrigation_needed', 'created_at'
    ]
    list_filter = [
        'crop_condition', 'pest_observed', 'irrigation_needed', 'created_at'
    ]
    search_fields = ['user__email', 'crop_type', 'notes']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Report Info', {
            'fields': ('user', 'crop_type')
        }),
        ('Condition', {
            'fields': ('crop_condition', 'pest_observed', 'irrigation_needed')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
