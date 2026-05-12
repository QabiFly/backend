from django.urls import path

from . import views

app_name = "gismap"

urlpatterns = [
    path('landmarks/', views.GISLandmarkListView.as_view(), name='gis-landmark-list'),
    path('landmarks/create/', views.GISLandmarkCreateView.as_view(), name='gis-landmark-create'),
    path('landmarks/<uuid:pk>/', views.GISLandmarkDetailView.as_view(), name='gis-landmark-detail'),
    path('weather-zones/', views.WeatherZoneListView.as_view(), name='weather-zone-list'),
    path('weather-zones/create/', views.WeatherZoneCreateView.as_view(), name='weather-zone-create'),
]
