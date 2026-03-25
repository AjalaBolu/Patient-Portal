from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    marital_status = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_full_name()
