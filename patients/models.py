from django.db import models
from staff import models as staff

gender_options = [('Male', 'male'), ('Female', 'female')]

# Create your models here.
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=gender_options)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    address = models.TextField(blank=False, null=False)
    #vitals = models.OneToOneField('Vitals', on_delete=models.CASCADE, null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    #emergency_contact = models.OneToOneField('EmergencyContact', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + str(self.patient_id)


class Vitals(models.Model):
    vitals_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vitals_detail')
    temperature = models.DecimalField(max_digits=5, decimal_places=2) # in degrees celsius
    blood_pressure = models.CharField(max_length=15) #systolic/diastolic in mmHg(120/80)
    heart_rate = models.IntegerField() #beats per minute
    respiratory_rate = models.IntegerField() #breaths per minute
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # in kilograms(kg)
    height = models.DecimalField(max_digits=5, decimal_places=2)  # in meters(m)
    #bmi = models.DecimalField(max_digits=5, decimal_places=2)  # calculate from weight and height

    def __str__(self):
        return f'Vitals for {self.patient.patient_id}'
    
    @property
    def bmi(self):
        if self.weight and self.height:
            return round(float(self.weight) / (float(self.height) ** 2), 2)
        return None


class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(staff.Doctor, on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=500, null=True, blank=True)
    diagnosis = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        ordering = ['-record_id']

    def __str__(self):
        return f'MR{self.record_id} - {self.patient.patient_id}'


class EmergencyContact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='emergency_contact')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.patient.patient_id}'


# class Doctor(models.Model):
#     doctor_id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField()
#     specialty = models.CharField(max_length=100)
#     gender = models.CharField(max_length=6, choices=gender_options)
#     phone_number = models.CharField(max_length=15, null=True, blank=True)
#     email = models.EmailField(null=True, blank=True)
#     address = models.TextField()


class CheckIn(models.Model):
    checkin_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(staff.Doctor, on_delete=models.PROTECT)
    checkin_time = models.DateTimeField(auto_now_add=True)
    checkout_time = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.patient.patient_id} - {self.patient.first_name} {self.patient.last_name}'
    #order by check in time, most recent first
    class Meta:
        ordering = ['-checkin_time']

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(staff.Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.patient.patient_id} - {self.date} {self.time}'