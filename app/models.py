from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    skills = models.CharField( max_length=500)
    languages = models.CharField(max_length= 500, blank=True)

# Create your models here.
