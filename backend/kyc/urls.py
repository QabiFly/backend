from django.urls import path

from . import views

app_name = "kyc"

urlpatterns = [
    path('', views.KYCDetailView.as_view(), name='kyc-detail'),
    path('upload/', views.KYCUploadView.as_view(), name='kyc-upload'),
    path('admin/list/', views.KYCAdminListView.as_view(), name='kyc-admin-list'),
    path('admin/<uuid:pk>/approve/', views.KYCApproveView.as_view(), name='kyc-admin-approve'),
    path('admin/<uuid:pk>/reject/', views.KYCRejectView.as_view(), name='kyc-admin-reject'),
]
