# app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('tutor', 'Tutor'),
        ('student', 'Student'),
    ]
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500)
    languages = models.CharField(max_length=500, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    languages_taught = models.CharField(max_length=500, blank=True)
    languages_learned = models.CharField(max_length=500, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)  # New field
