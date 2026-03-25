from django.db import models
from patients.models import Patient

class BillingRecord(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='billing_records')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient} - {self.amount} - {self.status}'

