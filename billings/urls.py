from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.billing_list, name='billing_list'),
    path('add/', views.billing_add, name='billing_add'),
    path('edit/<int:pk>/', views.billing_edit, name='billing_edit'),
    path('delete/<int:pk>/', views.billing_delete, name='billing_delete'),
    path('bills/export/', views.export_bills_csv, name='export_bills_csv'),
    path('mark-paid/<int:pk>/', views.billing_mark_paid, name='billing_mark_paid'),
    path('summary/<int:patient_id>/', views.billing_summary, name='billing_summary'),
]
