from django.urls import path
from . import views
from .views import admin_dashboard

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('', views.dashboard_home, name='dashboard_home'),
    path('', admin_dashboard, name='dashboard')
]
