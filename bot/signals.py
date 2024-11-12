from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(post_save, sender=Appointment)
def send_appointment_email(sender, instance, created, **kwargs):
    if created:
        subject = f'New {instance.speciality} Appointment'
        admin_content = render_to_string('appointment_admin_email.html', {'appointment': instance})

        emails = [
            (EmailMultiAlternatives(
                subject,
                'Appointment details are in HTML format. Please enable HTML to view.',
                'ikemoyo28@gmail.com',
                ['ikemoyo28@gmail.com'],
            ), admin_content)
        ]

        for email in emails:
            email[0].attach_alternative(email[1], mimetype='text/html')
            email[0].send()
