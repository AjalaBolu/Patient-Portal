from django import forms
from .models import BillingRecord

class BillingRecordForm(forms.ModelForm):
    class Meta:
        model = BillingRecord
        fields = ['patient', 'amount', 'description', 'status']
