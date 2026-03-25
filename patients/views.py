from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PatientForm
from .models import Patient
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from medical.models import LabResult, Prescription, MedicalHistory



def is_admin(user):
    return user.is_staff



@login_required
@user_passes_test(is_admin)
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)

            # Extract fields needed to create User
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # Create User
            user = User.objects.create_user(
                username=first_name.lower(),
                password='password1',
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Link user to patient and save
            patient.user = user
            patient.save()
            return redirect('patients')
    else:
        form = PatientForm()
    return render(request, 'patients/add_patient.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def patient_list(request):
    patients = Patient.objects.select_related('user').all()
    return render(request, 'patients/patient_list.html', {'patients': patients})


@login_required
@user_passes_test(is_admin)
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            # Update user info
            patient.user.first_name = form.cleaned_data['first_name']
            patient.user.last_name = form.cleaned_data['last_name']
            patient.user.email = form.cleaned_data['email']
            patient.user.save()

            form.save()  # Saves Patient (without touching user again)
            return redirect('patients:patients')
    else:
        # Pre-populate User data
        form = PatientForm(instance=patient, initial={
            'first_name': patient.user.first_name,
            'last_name': patient.user.last_name,
            'email': patient.user.email,
        })

    return render(request, 'patients/patient_form.html', {'form': form})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        user = patient.user
        patient.delete()
        user.delete()  # Also delete the associated user account
        messages.success(request, "Patient deleted successfully.")
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})

@login_required
@user_passes_test(is_admin)
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    lab_results = LabResult.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(patient=patient)
    medical_histories = MedicalHistory.objects.filter(patient=patient)

    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'lab_results': lab_results,
        'prescriptions': prescriptions,
        'medical_histories': medical_histories
    })

