from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment
from .forms import AppointmentForm
from patients.models import Patient
from .forms import EmergencyAppointmentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def appointment_list(request):
    appointments = Appointment.objects.all()
    doctors = User.objects.filter(groups__name='Doctors')  

    status = request.GET.get('status')
    doctor_id = request.GET.get('doctor')

    if status:
        appointments = appointments.filter(status=status)
    if doctor_id:
        appointments = appointments.filter(doctor__id=doctor_id)

    context = {
        'appointments': appointments,
        'doctors': doctors,
    }
    return render(request, 'appointments/appointment_list.html', context)
def appointment_add(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment:appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form})

def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        return redirect('appointment:appointment_list')
    return render(request, 'appointments/appointment_form.html', {'form': form})

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment:appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})

def emergency_appointment_request(request):
    if request.method == 'POST':
        form = EmergencyAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.is_emergency = True
            appointment.status = 'Scheduled'
            appointment.save()
            messages.success(request, 'Emergency appointment created successfully.')
            return redirect('appointment:appointment_list')
    else:
        form = EmergencyAppointmentForm()

    return render(request, 'appointments/emergency_appointment.html', {'form': form})

def request_emergency_appointment(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        return redirect('login')  # Or a suitable fallback

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.status = 'Pending'
            appointment.save()

            # Send email to admin/staff
            send_mail(
                subject='New Emergency Appointment Request',
                message=f"A new emergency appointment was requested by {patient.user.get_full_name()}.\n"
                        f"Reason: {appointment.reason}\n"
                        f"Date: {appointment.date}\n"
                        f"Doctor: {appointment.doctor.get_full_name()}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['admin@example.com'],  # Change to real staff/admin email(s)
                fail_silently=False,
            )

            return redirect('appointment:appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/request_emergency.html', {'form': form})

