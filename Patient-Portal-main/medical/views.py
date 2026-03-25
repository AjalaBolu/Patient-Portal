from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from .models import MedicalRecord, Prescription, LabResult, MedicalHistory
from .forms import MedicalRecordForm, PrescriptionForm, LabResultForm, MedicalHistoryForm
from patients.models import Patient


def is_admin(user):
    return user.is_staff


# MEDICAL RECORD VIEWS
@login_required
@user_passes_test(is_admin)
def medical_list(request):
    records = MedicalRecord.objects.select_related('patient').all()
    return render(request, 'medical/medical_list.html', {'records': records})


@login_required
@user_passes_test(is_admin)
def medical_add(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical:medical_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'medical/medical_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def medical_edit(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('medical:medical_list')
    else:
        form = MedicalRecordForm(instance=record)
    return render(request, 'medical/medical_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def medical_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('medical:medical_list')
    return render(request, 'medical/medical_confirm_delete.html', {'record': record})


# PRESCRIPTION VIEWS
@login_required
@user_passes_test(is_admin)
def prescription_all(request):
    query = request.GET.get('q', '')
    prescriptions = Prescription.objects.select_related('patient__user').all()

    if query:
        prescriptions = prescriptions.filter(
            Q(patient__user__first_name__icontains=query) |
            Q(patient__user__last_name__icontains=query) |
            Q(medication__icontains=query)
        )

    patients = Patient.objects.select_related('user').all()
    return render(request, 'medical/prescription_all.html', {
        'prescriptions': prescriptions,
        'patients': patients,
        'query': query
    })


@login_required
@user_passes_test(is_admin)
def prescription_list(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    prescriptions = Prescription.objects.filter(patient=patient)
    return render(request, "medical/prescription_list.html", {
        "patient": patient,
        "prescriptions": prescriptions,
    })

@login_required
@user_passes_test(is_admin)
def prescription_add(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            prescription.save()
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = PrescriptionForm()
    return render(request, 'medical/prescription_form.html', {'form': form, 'patient': patient})


@login_required
@user_passes_test(is_admin)
def prescription_edit(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('medical:prescription_list')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'medical/prescription_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    patient_id = prescription.patient.id  # 🔑 grab patient ID

    if request.method == "POST":
        prescription.delete()
        return redirect("medical:prescription_list", patient_id=patient_id)  # ✅ include patient_id

    return render(request, "medical/prescription_confirm_delete.html", {"prescription": prescription})


# LAB RESULT VIEWS
@login_required
@user_passes_test(is_admin)
def labresult_all(request):
    query = request.GET.get('q', '')
    results = LabResult.objects.select_related('patient__user').all()

    if query:
        results = results.filter(
            Q(patient__user__first_name__icontains=query) |
            Q(patient__user__last_name__icontains=query) |
            Q(test_name__icontains=query)
        )

    patients = Patient.objects.select_related('user').all()
    return render(request, 'medical/labresult_all.html', {
        'results': results,
        'patients': patients,
        'query': query
    })


@login_required
@user_passes_test(is_admin)
def labresult_list(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    results = LabResult.objects.filter(patient=patient)
    return render(request, 'medical/labresult_list.html', {
        'results': results,
        'patient': patient
    })


@login_required
@user_passes_test(is_admin)
def labresult_add(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = LabResultForm(request.POST, request.FILES)
        if form.is_valid():
            lab_result = form.save(commit=False)
            lab_result.patient = patient
            lab_result.save()
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = LabResultForm()
    return render(request, 'medical/labresult_form.html', {'form': form, 'patient': patient})


@login_required
@user_passes_test(is_admin)
def labresult_edit(request, pk):
    labresult = get_object_or_404(LabResult, pk=pk)
    if request.method == 'POST':
        form = LabResultForm(request.POST, request.FILES, instance=labresult)
        if form.is_valid():
            form.save()
            return redirect('medical:labresult_list', patient_id=labresult.patient.pk)
    else:
        form = LabResultForm(instance=labresult)
    return render(request, 'medical/labresult_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def labresult_delete(request, pk):
    labresult = get_object_or_404(LabResult, pk=pk)
    if request.method == 'POST':
        labresult.delete()
        return redirect('medical:labresult_list', patient_id=labresult.patient.pk)
    return render(request, 'medical/labresult_confirm_delete.html', {'labresult': labresult})


# MEDICAL HISTORY VIEWS
@login_required
@user_passes_test(is_admin)
def medicalhistory_all(request):
    query = request.GET.get('q', '')
    histories = MedicalHistory.objects.select_related('patient__user').all()

    if query:
        histories = histories.filter(
            Q(patient__user__first_name__icontains=query) |
            Q(patient__user__last_name__icontains=query) |
            Q(condition__icontains=query)
        )

    patients = Patient.objects.select_related('user').all()
    return render(request, 'medical/medicalhistory_all.html', {
        'histories': histories,
        'patients': patients,
        'query': query
    })



@login_required
@user_passes_test(is_admin)
def medicalhistory_add(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.patient = patient
            history.save()
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = MedicalHistoryForm()
    return render(request, 'medical/medicalhistory_form.html', {'form': form, 'patient': patient})


@login_required
@user_passes_test(is_admin)
def medicalhistory_edit(request, pk):
    history = get_object_or_404(MedicalHistory, pk=pk)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            return redirect('patients:patient_detail', pk=history.patient.pk)
    else:
        form = MedicalHistoryForm(instance=history)
    return render(request, 'medical/medicalhistory_form.html', {'form': form, 'patient': history.patient})


@login_required
@user_passes_test(is_admin)
def medicalhistory_delete(request, pk):
    history = get_object_or_404(MedicalHistory, pk=pk)
    patient = history.patient
    if request.method == 'POST':
        history.delete()
        return redirect('patients:patient_detail', pk=patient.pk)
    return render(request, 'medical/medicalhistory_confirm_delete.html', {'history': history})
