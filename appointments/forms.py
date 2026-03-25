# forms.py
from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'reason', 'status']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EmergencyAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'reason']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }