#import send_mail
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from staff.models import Doctor

#send registration email for new patients
def send_registration_email(email):
    if email:
        try:
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            return
        else:
            subject = 'Registration Confirmation'
            message = f'''Dear {patient.first_name},\n
            Welcome to the Hospital Management System. Kindly find your details below: \n
            Name: {patient.first_name} {patient.last_name}\n
            Email: {patient.email}\n
            Phone Number: {patient.phone_number}\n
            Address: {patient.address}\n
            Date of Birth: {patient.date_of_birth}\n
            Occupation: {patient.occupation}\n\n
            Thank you for registering with us.\n      
    '''
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

#send appointment email to patients and doctor
def send_appointment_email(email, doctor_email, date, time):
    doctor = Doctor.objects.get(email=doctor_email)
    subject = 'Appointment Confirmation'
    patient = Patient.objects.get(email=email)
    # if email:
    #     patient = Patient.objects.get(email=email)

    #     #add appointment date and time to the message sent to patient
    #     message = f'''Your appointment has been scheduled successfully. Details are as follows\n
    #     Patient Name: {patient.first_name} {patient.last_name}\n
    #     Patient id: {patient.patient_id}\n
    #     Doctor: {doctor.first_name} {doctor.last_name}\n
    #     Date: {date}\n
    #     Time: {time}\n
    #     '''
    #     send_mail(subject, message, settings.EMAIL_HOST_USER, [email],fail_silently=False)      

    #add appointment date and time to the message sent to doctor
    message = f'''An appointment has been added. Details are as follows:\n
    Patient Name: {patient.first_name} {patient.last_name}\n
    Patient id: {patient.patient_id}\n
    Doctor: {doctor.first_name} {doctor.last_name}\n
    Date: {date}\n
    Time: {time}\n
    '''
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email,doctor_email],fail_silently=False)  