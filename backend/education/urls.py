from django.urls import path

from . import views

app_name = "education"

urlpatterns = [
    path('', views.education_home, name='education-home'),
    path('courses/', views.education_courses, name='education-courses'),
    path('live-classes/', views.education_live_classes, name='education-live-classes'),
    path('enroll/', views.education_enroll, name='education-enroll'),
]
