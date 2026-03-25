from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import BillingRecord
from .forms import BillingRecordForm
from patients.models import Patient
from django.db.models import Q
import csv
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib import messages


def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def billing_list(request):
    status = request.GET.get('status')
    patient_id = request.GET.get('patient')
    query = request.GET.get('q')

    records = BillingRecord.objects.select_related('patient__user').all()

    if status:
        records = records.filter(status=status)

    if patient_id:
        records = records.filter(patient_id=patient_id)

    if query:
        records = records.filter(
            Q(description__icontains=query) |
            Q(patient__user__first_name__icontains=query) |
            Q(patient__user__last_name__icontains=query)
        )

    patients = Patient.objects.all()

    return render(request, 'billing/billing_list.html', {
        'records': records,
        'patients': patients,
    })


@login_required
@user_passes_test(is_admin)
def billing_add(request):
    if request.method == 'POST':
        form = BillingRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('billing:billing_list')
    else:
        form = BillingRecordForm()
    return render(request, 'billing/billing_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def billing_edit(request, pk):
    record = get_object_or_404(BillingRecord, pk=pk)
    if request.method == 'POST':
        form = BillingRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('billilng:billing_list')
    else:
        form = BillingRecordForm(instance=record)
    return render(request, 'billing/billing_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def billing_delete(request, pk):
    record = get_object_or_404(BillingRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('billing:billing_list')
    return render(request, 'billing/billing_confirm_delete.html', {'record': record})

def billing_mark_paid(request, pk):
    billing = get_object_or_404(BillingRecord, pk=pk)
    billing.status = 'paid'
    billing.save()
    return redirect('billing_list')




def export_bills_csv(request):
    query = request.GET.get("q", "")
    status = request.GET.get("status", "")

    bills = BillingRecord.objects.select_related('patient').all()

    if query:
        bills = bills.filter(
            Q(patient__user__first_name__icontains=query) |
            Q(patient__user__last_name__icontains=query) |
            Q(description__icontains=query)
        )

    if status:
        bills = bills.filter(status=status)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="bills_export.csv"'

    writer = csv.writer(response)
    writer.writerow(["Patient", "Description", "Amount", "Status", "Date Issued"])

    for bill in bills:
        writer.writerow([
            bill.patient.user.get_full_name(),
            bill.description,
            bill.amount,
            bill.status,
            bill.date_issued.strftime("%Y-%m-%d")
        ])

    return response


def billing_summary(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    records = BillingRecord.objects.filter(patient=patient)

    total_amount = records.aggregate(total=Sum('amount'))['total'] or 0
    paid_amount = records.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    unpaid_amount = records.filter(status='unpaid').aggregate(total=Sum('amount'))['total'] or 0
    pending_amount = records.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'patient': patient,
        'records': records,
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'unpaid_amount': unpaid_amount,
        'pending_amount': pending_amount,
    }
    return render(request, 'billing/billing_summary.html', context)

def billing_mark_paid(request, pk):
    """Mark a billing record as paid."""
    billing_record = get_object_or_404(BillingRecord, pk=pk)
    
    if billing_record.status != 'paid':
        billing_record.status = 'paid'
        billing_record.save()
        messages.success(request, f'Billing record for {billing_record.patient.user.get_full_name()} marked as paid.')
    else:
        messages.info(request, 'This billing record is already paid.')
    
    return redirect('billing:billing_list')