from django.urls import path

from . import views

app_name = "delivery"

urlpatterns = [
    path('boys/', views.DeliveryBoyListView.as_view(), name='delivery-boy-list'),
    path('boys/create/', views.DeliveryBoyCreateView.as_view(), name='delivery-boy-create'),
    path('boys/<uuid:pk>/', views.DeliveryBoyDetailView.as_view(), name='delivery-boy-detail'),
    path('assignments/', views.DeliveryAssignmentListView.as_view(), name='delivery-assignment-list'),
    path('assignments/<uuid:pk>/accept/', views.DeliveryAssignmentAcceptView.as_view(), name='delivery-assignment-accept'),
    path('assignments/<uuid:pk>/verify-otp/', views.DeliveryAssignmentVerifyOTPView.as_view(), name='delivery-assignment-verify-otp'),
    path('locations/', views.DeliveryLocationListView.as_view(), name='delivery-location-list'),
    path('locations/update/', views.DeliveryLocationUpdateView.as_view(), name='delivery-location-update'),
]
