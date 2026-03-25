from django.db import models
from patients.models import Patient
from django.contrib.auth.models import User

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    allergies = models.TextField(blank=True, null=True)  # ✅ Add this
    notes = models.TextField(blank=True, null=True)      # ✅ Add this
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.diagnosis}"
    
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_prescribed = models.DateField(auto_now_add=True)
    medication = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.medication} for {self.patient.user.get_full_name()}"

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    result = models.TextField()
    date_conducted = models.DateField()
    file = models.FileField(upload_to='lab_results/', blank=True, null=True)  # Optional upload

    def __str__(self):
        return f"{self.test_name} - {self.patient.user.get_full_name()}"

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255)
    treatment = models.TextField()
    date_diagnosed = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.condition}"
    

class PrescriptionRefillRequest(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="refill_requests")
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("denied", "Denied")],
        default="pending"
    )

    def __str__(self):
        return f"Refill Request for {self.prescription.medication} ({self.patient.username})"

class LabTestRequest(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lab_test_requests")
    test_name = models.CharField(max_length=255)
    reason = models.TextField()
    requested_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("denied", "Denied")],
        default="pending"
    )

    def __str__(self):
        return f"{self.test_name} request ({self.patient.username})"