#import send_mail
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import *
from staff.models import Doctor
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#send registration email for new patients
# def send_registration_email(email):
#     if email:
#         try:
#             patient = Patient.objects.get(email=email)
#         except Patient.DoesNotExist:
#             return
#         else:
#             subject = 'Registration Confirmation'
#             message = f'''Dear {patient.first_name},\n
#             Welcome to the Hospital Management System. Kindly find your details below: \n
#             Name: {patient.first_name} {patient.last_name}\n
#             Email: {patient.email}\n
#             Phone Number: {patient.phone_number}\n
#             Address: {patient.address}\n
#             Date of Birth: {patient.date_of_birth}\n
#             Occupation: {patient.occupation}\n\n
#             Thank you for registering with us.\n      
#     '''
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

#send appointment email to patients and doctor
def send_appointment_email(email, doctor_email, date, time):
    doctor = Doctor.objects.get(email=doctor_email)
    subject = 'Appointment Confirmation'
    patient = Patient.objects.get(email=email)
    
    html_message = render_to_string('appointment_email.html', {
        'patient': patient.first_name,
        'doctor': doctor.first_name + ' ' + doctor.last_name,
        'date': date,
        'time': time
    })
    plain_message = strip_tags(html_message)
    
    message = EmailMultiAlternatives(subject=subject, body=plain_message, from_email=settings.EMAIL_HOST_USER, to=[email, doctor_email])

    message.attach_alternative(html_message, "text/html")
    message.send()