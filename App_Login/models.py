from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    SEX_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ]
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='User_Profile')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True) 
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)


class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)

    def __str__(self):
        return self.username



