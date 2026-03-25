from django.db import models
from patients.models import Patient
from django.contrib.auth.models import User

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_staff': True})
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    is_emergency = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.date.strftime('%Y-%m-%d %H:%M')}"
