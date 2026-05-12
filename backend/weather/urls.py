from django.urls import path

from . import views

app_name = "weather"

urlpatterns = [
    path('data/', views.WeatherDataListView.as_view(), name='weather-data-list'),
    path('data/create/', views.WeatherDataCreateView.as_view(), name='weather-data-create'),
    path('data/<uuid:pk>/', views.WeatherDataDetailView.as_view(), name='weather-data-detail'),
    path('field-reports/', views.FarmerFieldReportListView.as_view(), name='field-report-list'),
    path('field-reports/create/', views.FarmerFieldReportCreateView.as_view(), name='field-report-create'),
    path('current/', views.CurrentWeatherView.as_view(), name='current-weather'),
    path('forecast/', views.WeatherForecastView.as_view(), name='weather-forecast'),
    path('crop-advice/', views.CropAdviceView.as_view(), name='crop-advice'),
]
