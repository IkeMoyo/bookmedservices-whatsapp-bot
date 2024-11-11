from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import time


class Organisation(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Appointment(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    speciality = models.CharField(max_length=50)
    reason = models.TextField()
    date = models.DateField(
        validators=[
            MinValueValidator(limit_value=timezone.now().date())
        ]
    )
    time = models.TimeField()
    status_choices = [
        ('Scheduled', 'Scheduled'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment {self.id} - {self.customer.first_name} {self.customer.last_name} with {self.organisation.name}"

    def validate_time_range(value):

        if not (time(9, 0) <= value <= time(17, 0)):
            raise ValidationError('Time must be between 9 AM and 5 PM.')

        if value.minute % 30 != 0:
            raise ValidationError('Time must be in 30-minute intervals.')
