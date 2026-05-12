from django.urls import path

from . import views

app_name = "emi"

urlpatterns = [
    path('', views.EMIListView.as_view(), name='emi-list'),
    path('create/', views.EMICreateView.as_view(), name='emi-create'),
    path('<uuid:pk>/', views.EMIDetailView.as_view(), name='emi-detail'),
    path('<uuid:pk>/pay/', views.EMIPayView.as_view(), name='emi-pay'),
]
