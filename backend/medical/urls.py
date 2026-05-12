from django.urls import path

from . import views

app_name = "medical"

urlpatterns = [
    path('', views.medical_home, name='medical-home'),
    path('register/', views.medical_register, name='medical-register'),
    path('appointments/', views.medical_appointments, name='medical-appointments'),
    path('pharmacies/', views.medical_pharmacies, name='medical-pharmacies'),
]
