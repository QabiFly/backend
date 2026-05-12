from django.urls import path

from . import views

app_name = "khata"

urlpatterns = [
    path('udhaar/', views.UdhaarListView.as_view(), name='udhaar-list'),
    path('udhaar/create/', views.UdhaarCreateView.as_view(), name='udhaar-create'),
    path('udhaar/<uuid:pk>/pay/', views.UdhaarPayView.as_view(), name='udhaar-pay'),
    path('sunday-collections/', views.SundayCollectionView.as_view(), name='sunday-collection-list'),
    path('sunday-collections/create/', views.SundayCollectionCreateView.as_view(), name='sunday-collection-create'),
    path('sunday-collections/<uuid:pk>/collect/', views.SundayCollectionCollectView.as_view(), name='sunday-collection-collect'),
]
