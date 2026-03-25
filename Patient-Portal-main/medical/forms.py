from django import forms
from .models import MedicalRecord
from .models import Prescription
from .models import LabResult
from .models import MedicalHistory
from .models import PrescriptionRefillRequest
from .models import LabTestRequest

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'dosage', 'instructions']


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'diagnosis', 'treatment', 'allergies', 'notes']


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'dosage', 'instructions']


class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['patient', 'test_name', 'result', 'date_conducted', 'file']


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['condition', 'treatment', 'date_diagnosed', 'notes']

class PrescriptionRefillRequestForm(forms.ModelForm):
    class Meta:
        model = PrescriptionRefillRequest
        fields = ["prescription"]

class LabTestRequestForm(forms.ModelForm):
    class Meta:
        model = LabTestRequest
        fields = ["test_name", "reason"]
        widgets = {
            "test_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Blood Test"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Why do you need this test?"}),
        }

