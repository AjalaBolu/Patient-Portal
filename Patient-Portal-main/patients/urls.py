from django.urls import path
from . import views


app_name = 'patients'

urlpatterns = [
    path('add/', views.add_patient, name='add_patient'),
    path('', views.patient_list, name='patients'),
    path('edit/<int:pk>/', views.patient_edit, name='patient_edit'), 
    path('<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
]
