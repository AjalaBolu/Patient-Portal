from django.urls import path
from . import views


app_name = 'patient_portal'

urlpatterns = [
    path('login/', views.patient_login, name='patient_login'),
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('logout/', views.patient_logout, name='patient_logout'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('profiles/update-picture/', views.update_profile_picture, name='update_profile_picture'),

    # Medical
    path('medical-records/', views.medical_records, name='patient_medical_records'),
    path('lab-results/', views.lab_results, name='patient_lab_results'),
    path('lab-results/request/', views.lab_result_request, name='lab_result_request'),
    path('prescriptions/', views.prescriptions, name='patient_prescriptions'),
    path('prescriptions/<int:pk>/request-refill/', views.request_refill, name='request_refill'),

    # Messaging
    path('messages/', views.my_messages, name='patient_messages'),
    path('messages/compose/', views.patient_message_compose, name='patient_message_compose'),

    # Appointments
    path('appointments/', views.appointments, name='patient_appointments'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='patient_appointment_detail'),
    path('appointments/<int:appointment_id>/cancel/', views.appointment_cancel, name='patient_appointment_cancel'),
    path('appointment/request/', views.appointment_request, name='patient_appointment_request'),
]
