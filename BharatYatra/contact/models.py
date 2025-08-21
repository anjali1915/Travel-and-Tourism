from django.db import models
from django.core.validators import RegexValidator

class ContactData(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, validators=[
                                    RegexValidator(r'^\d{10}$')
                                    ])
    email = models.EmailField(max_length=254, unique=True)
    message = models.CharField(max_length=500)

def __str__(self):
        return self.name

# Create your models here.
