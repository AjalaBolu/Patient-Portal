from django.shortcuts import render
from django.shortcuts import render
from appointments.models import Appointment
from patients.models import Patient
from billings.models import BillingRecord
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from patients.models import Patient
from appointments.models import Appointment
from billings.models import BillingRecord
from medical.models import Prescription, LabResult, MedicalHistory
from django.utils import timezone
from medical.models import MedicalRecord, Prescription, LabResult

@login_required
def admin_dashboard(request):
    context = {
        'new_patients_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
        'lab_result_count': LabResult.objects.count(),
        'prescription_count': Prescription.objects.count(),
        'admitted_count': Patient.objects.filter(status='admitted').count(),
        'discharged_count': Patient.objects.filter(status='discharged').count(),
        'medical_history_count': MedicalRecord.objects.count(),
        'billing_count': BillingRecord.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)
@login_required
def dashboard_home(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_lab_results': LabResult.objects.count(),
        'total_prescriptions': Prescription.objects.count(),
        'total_bills': BillingRecord.objects.count(),
        'recent_activity': []
    }
    return render(request, 'dashboard/dashboard_home.html', context)