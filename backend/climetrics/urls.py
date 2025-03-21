from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as django_auth_views  # Rename to avoid conflict
from authentication import views as auth_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_views.home, name='home'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('los-comparison/', dashboard_views.los_comparison, name='los_comparison'),
    path('complication-rates/', dashboard_views.complication_rates, name='complication_rates'),
    path('stage-distribution/', dashboard_views.stage_distribution, name='stage_distribution'),
    path('surgeon-rates/', dashboard_views.surgeon_rates, name='surgeon_rates'),
    path('users/', dashboard_views.users_list, name='users_list'),
    
    # Authentication URLs - use Django's built-in views
    path('login/', django_auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register, name='register'),
    
    # Include Django auth URLs for additional auth views (password reset, etc.)
    path('', include('django.contrib.auth.urls')),
] 