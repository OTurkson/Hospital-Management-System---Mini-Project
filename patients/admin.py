from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Patient)
admin.site.register(EmergencyContact)
admin.site.register(Vitals)
admin.site.register(MedicalRecord)
admin.site.register(CheckIn)
admin.site.register(Appointment)
