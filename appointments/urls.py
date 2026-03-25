from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('add/', views.appointment_add, name='appointment_add'),
    path('edit/<int:pk>/', views.appointment_edit, name='appointment_edit'),
    path('delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),
    path('emergency/', views.emergency_appointment_request, name='emergency_appointment'),
    path('appointments/request/', views.request_emergency_appointment, name='request_emergency'),
]
