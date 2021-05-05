from django.urls import path

from . import views

urlpatterns = [
    path('mean', views.calculate_mean, name='calculate_mean'),
    path('tendency', views.central_tendency, name='tendency')
]