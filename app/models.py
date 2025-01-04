# app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500)
    languages = models.CharField(max_length=500, blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    role = models.CharField(choices=[('tutor', 'Tutor'), ('student', 'Student'), ('both', 'Both')], default='student', max_length=10)

class Tutor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    students = models.ManyToManyField('Student', related_name='tutors', blank=True)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    max_budget = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True)

class StudentTutorRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    status = models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
