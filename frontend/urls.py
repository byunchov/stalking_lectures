from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('analysis/', views.analysis_list_view, name='analysis'),
    path('analysis/<int:upload_id>/', views.analysis_main_view, name='analysis_item'),
    path('analysis/<int:upload_id>/spread/', views.analysis_spread_view, name='spread'),
]