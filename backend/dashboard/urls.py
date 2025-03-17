from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('los-comparison/', views.los_comparison, name='los_comparison'),
    path('complication-rates/', views.complication_rates, name='complication_rates'),
    path('stage-distribution/', views.stage_distribution, name='stage_distribution'),
    path('surgeon-rates/', views.surgeon_rates, name='surgeon_rates'),
] 