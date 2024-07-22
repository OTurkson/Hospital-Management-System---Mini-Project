from django.db import models

gender_options = [('Male', 'male'), ('Female', 'female')]

#Create your models here.
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    specialty = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=gender_options)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'