from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    email = forms.EmailField(label="Email")

    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'phone',
            'address',
            'marital_status',
            'emergency_contact',
            'emergency_phone',
            'email',
        ]
