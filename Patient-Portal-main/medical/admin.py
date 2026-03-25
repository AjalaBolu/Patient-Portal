

# Register your models here.
# medical/admin.py
from django.contrib import admin
from .models import MedicalRecord
from .models import LabResult

admin.site.register(MedicalRecord)
admin.site.register(LabResult)
