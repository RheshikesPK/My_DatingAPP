from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    SMOKE = (
        ('N','Non-Smoker'),
        ('O','Occasional Smoker'),
        ('R','Regular Smoker')
    )
    REL_STATAS = (
        ('S','Single'),
        ('M','Married'),
        ('W','Widow'),
        ('D','Divorced'),
    )
    DRINKING = (
        ('N','Non-Drinker'),
        ('O','Ocaasional Drinker'),
        ('R','Regular Drinker'),
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    qualification = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    bio=models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    smoke = models.CharField(max_length=1,choices=SMOKE,default='N')
    drinking = models.CharField(max_length=1,choices=DRINKING,default='N')
    rel_status = models.CharField(max_length=1, choices=REL_STATAS,default='S')
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, default=None)
    short_reel = models.FileField(upload_to='short_reels/', null=True, default=None)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self) -> str:
        return self.username

class EmployeeEmployer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_field = models.CharField(max_length=100)
    experience = models.CharField(max_length=1, choices=[
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('E', 'Expert'),
        
    ],default='B',)

    def __str__(self):
        return f"{self.user.username} - {self.job_field}"
    

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.district}, {self.state}, {self.pincode}, {self.country}"
    

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'