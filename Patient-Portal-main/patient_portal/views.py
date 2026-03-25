# patient_portal/views.py
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from medical.models import MedicalRecord, LabResult, Prescription, LabTestRequest
from communications.models import Message
from appointments.models import Appointment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from billings.models import BillingRecord
from .forms import AppointmentRequestForm
from .forms import MessageForm
from .models import Profile
from .forms import ProfilePictureForm
from medical.models import Prescription, PrescriptionRefillRequest
from medical.forms import PrescriptionRefillRequestForm
from medical.forms import LabTestRequestForm

def patient_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ✅ Only allow patients
            if hasattr(user, "patient"):
                login(request, user)
                return redirect(reverse("patient_portal:patient_dashboard"))
            else:
                messages.error(request, "Only patients can log in here.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "patient_portal/login.html")

@login_required(login_url='/patient_portal/login')
def patient_dashboard(request):
    # Ensure only patients access this dashboard
    if not hasattr(request.user, 'patient'):
        messages.error(request, "You are not authorized to access the patient dashboard.")
        return redirect('/')

    patient = request.user.patient  # Assuming OneToOneField from Patient to User

    # Recent records
    recent_medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-date_created')[:5]
    recent_prescriptions = Prescription.objects.filter(patient=patient).order_by('-date_prescribed')[:5]
    recent_lab_results = LabResult.objects.filter(patient=patient).order_by('-date_conducted')[:5]
    upcoming_appointments = Appointment.objects.filter(patient=patient, status='Scheduled').order_by('date')[:5]
    unpaid_bills = BillingRecord.objects.filter(patient=patient, status='Unpaid')

    context = {
        'patient': patient,
        'recent_medical_records': recent_medical_records,
        'recent_prescriptions': recent_prescriptions,
        'recent_lab_results': recent_lab_results,
        'upcoming_appointments': upcoming_appointments,
        'unpaid_bills': unpaid_bills,
    }
    return render(request, 'patient_portal/dashboard.html', context)

def patient_logout(request):
    logout(request)
    return redirect('patient_login')

@login_required
def my_profile(request):
    try:
        # fetch Patient instance linked to the logged-in user
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return redirect("dashboard")  # fallback if somehow not found

    # handle profile picture update
    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("my_profile")
    else:
        form = ProfilePictureForm(instance=patient)

    appointments = Appointment.objects.filter(patient=patient)
    billings = BillingRecord.objects.filter(patient=patient)
    profile = get_object_or_404(Patient, user=request.user)

    return render(request, "patient_portal/profile.html", {
        "patient": patient,
        "appointments": appointments,
        "billings": billings,
        "form": form,
        "profile": profile,
        "user": request.user
    })

@login_required
def medical_records(request):
    patient = Patient.objects.get(user=request.user)
    records = MedicalRecord.objects.filter(patient=patient)
    return render(request, "patient_portal/medical_records.html", {"records": records})

@login_required
def lab_results(request):
    try:
        patient = Patient.objects.get(user=request.user)  # <-- ensure this returns Patient instance
    except Patient.DoesNotExist:
        patient = None

    if patient:
        lab_results = LabResult.objects.filter(patient=patient).order_by('-date_conducted')
    else:
        lab_results = LabResult.objects.none()

    context = {
        'lab_results': lab_results,
    }
    return render(request, 'patient_portal/lab_results.html', context)

def lab_result_request(request):
    test_requests = LabTestRequest.objects.filter(patient=request.user)
    return render(request, "patient_portal/lab_result_request.html", {
        "test_requests": test_requests
    })

@login_required
def prescriptions(request):
    patient = Patient.objects.get(user=request.user)
    prescriptions = Prescription.objects.filter(patient=patient)
    return render(request, "patient_portal/prescriptions.html", {"prescriptions": prescriptions})

def my_messages(request):
    inbox = Message.objects.filter(recipient=request.user)
    sent = Message.objects.filter(sender=request.user)
    return render(request, 'patient_portal/messages.html', {
        'inbox': inbox,
        'sent': sent
    })
@login_required
def appointments(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, "patient_portal/appointments.html", {"appointments": appointments})

@login_required
def appointment_detail(request, appointment_id):
    # get the Patient object for the logged-in user
    patient = get_object_or_404(Patient, user=request.user)

    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)
    return render(request, 'patient_portal/appointment_detail.html', {'appointment': appointment})


@login_required
def appointment_request(request):
    if request.method == "POST":
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.status = "Pending"
            appointment.save()
            messages.success(request, "Your appointment request has been submitted.")
            return redirect("patient_portal:patient_appointment_list")
    else:
        form = AppointmentRequestForm()
    return render(request, "patient_portal/appointment_request.html", {"form": form})

@login_required
@login_required
def appointment_cancel(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if request.method == "POST":
        appointment.status = "Cancelled"
        appointment.save()
        return redirect('patient_portal:patient_appointments')
    return render(request, 'patient_portal/appointment_cancel_confirm.html', {'appointment': appointment})


def patient_message_compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('patient_messages')  # Back to inbox
    else:
        form = MessageForm()
    return render(request, 'patient_portal/message_compose.html', {'form': form})

@login_required
def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        profile = get_object_or_404(Profile, user=request.user)
        profile.profile_picture = request.FILES["profile_picture"]
        profile.save()
        messages.success(request, "Profile picture updated successfully.")
    else:
        messages.error(request, "No picture uploaded.")
    return redirect("patient_portal:my_profile")

@login_required
def request_refill(request):
    if request.method == "POST":
        form = PrescriptionRefillRequestForm(request.POST)
        if form.is_valid():
            refill_request = form.save(commit=False)
            refill_request.patient = request.user
            refill_request.save()
            return redirect("patient_portal:my_prescriptions")
    else:
        form = PrescriptionRefillRequestForm()

    prescriptions = Prescription.objects.filter(patient=request.user)
    return render(request, "patient_portal/request_refill.html", {
        "form": form,
        "prescriptions": prescriptions
    })

@login_required
def request_lab_test(request):
    if request.method == "POST":
        form = LabTestRequestForm(request.POST)
        if form.is_valid():
            test_request = form.save(commit=False)
            test_request.patient = request.user
            test_request.save()
            return redirect("patient_portal:my_lab_results")
    else:
        form = LabTestRequestForm()

    return render(request, "patient_portal/request_lab_test.html", {"form": form})