from django import forms
from appointments.models import Appointment
from communications.models import Message
from .models import Profile

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'placeholder': 'Describe your reason...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']