from django.contrib import admin
from django.urls import path, include
from authentication.views import logout_view, register
from dashboard.views import home, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('', include('django.contrib.auth.urls')),
] 