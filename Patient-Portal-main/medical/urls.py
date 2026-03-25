from django.urls import path
from . import views

app_name = 'medical'

urlpatterns = [
    path('', views.medical_list, name='medical_list'),
    path('add/', views.medical_add, name='medical_add'),
    path('edit/<int:pk>/', views.medical_edit, name='medical_edit'),
    path('delete/<int:pk>/', views.medical_delete, name='medical_delete'),
    path('prescriptions/', views.prescription_all, name='prescription_all'),
    path('prescriptions/<int:patient_id>/', views.prescription_list, name='prescription_list'),
    path('prescriptions/add/<int:patient_id>/', views.prescription_add, name='prescription_add'),
    path('prescriptions/edit/<int:pk>/', views.prescription_edit, name='prescription_edit'),
    path('prescriptions/delete/<int:pk>/', views.prescription_delete, name='prescription_delete'),
    path('labresults/', views.labresult_all, name='labresult_all'),
    path('labresults/<int:patient_id>/', views.labresult_list, name='labresult_list'),
    path('labresults/add/<int:patient_id>/', views.labresult_add, name='labresult_add'),
    path('labresults/edit/<int:pk>/', views.labresult_edit, name='labresult_edit'),
    path('labresults/delete/<int:pk>/', views.labresult_delete, name='labresult_delete'),
    path('medicalhistory/', views.medicalhistory_all, name='medicalhistory_all'),
    path('medicalhistory/add/<int:patient_id>/', views.medicalhistory_add, name='medicalhistory_add'),
    path('medicalhistory/edit/<int:pk>/', views.medicalhistory_edit, name='medicalhistory_edit'),
    path('medicalhistory/delete/<int:pk>/', views.medicalhistory_delete, name='medicalhistory_delete'),
]



