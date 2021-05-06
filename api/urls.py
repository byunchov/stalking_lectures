from django.urls import path

from . import views

urlpatterns = [
    path('', views.test, name='test'),
    path('mean', views.calculate_mean, name='calculate_mean'),
    path('tendency', views.central_tendency, name='tendency'),
    path('analysis', views.all_analysis, name='all_analysis')
]