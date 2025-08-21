from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True,
        null=True
    )
    phone = models.CharField(max_length=10, validators=[
        RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number')
    ])
    email = models.EmailField(unique=True)

def __str__(self):
        return self.username







































































