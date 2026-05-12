from django.urls import path

from . import views

app_name = "videos"

urlpatterns = [
    path('', views.VideoContentListView.as_view(), name='video-list'),
    path('create/', views.VideoContentCreateView.as_view(), name='video-create'),
    path('<uuid:pk>/', views.VideoContentDetailView.as_view(), name='video-detail'),
    path('<uuid:pk>/increment-view/', views.VideoContentViewIncrementView.as_view(), name='video-increment-view'),
]
