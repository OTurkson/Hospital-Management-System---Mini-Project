#send_registration emails to patients, doctors and admins when they are added to the system
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_registration_email(email):
    if email:
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return
        else:
            subject = 'Registration Confirmation'
            
            html_message = render_to_string('registration_email.html', {
                'user': user,
            })
            plain_message = strip_tags(html_message)
        
            message = EmailMultiAlternatives(subject=subject, body=plain_message, from_email=settings.EMAIL_HOST_USER, to=[user.email])

            message.attach_alternative(html_message, "text/html")
            message.send()