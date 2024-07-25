#send_registration emails to patients, doctors and admins when they are added to the system
from django.core.mail import send_mail
from django.conf import settings
from .models import *

def send_registration_email(email):
    if email:
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return
        else:
            subject = 'Registration Confirmation'
            message = f'''Dear {user.username},\n
            Welcome to the Hospital Management System. Kindly find your details below: \n
            Name: {user.username}\n
            Email: {user.email}\n
            Role: {user.role}\n\n
            Thank you for registering with us.\n      
    '''
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)