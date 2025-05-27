from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.


class User(AbstractUser): 
    Role_Choice=[
        ('learner',"Learner"),
        ('trainer',"Trainer"),
        ('admin',"Admin")
    ]

    date_joined=None

    role=models.CharField(max_length=155,choices=Role_Choice,default="learner")
    avatar=models.CharField(max_length=600)
    bio=models.TextField()
    created_at=models.DateTimeField(auto_now=True)
    email=models.EmailField(unique=True)
    is_email_verified=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username'] 


class PasswordResetOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp_code =models.CharField(max_length=6)
    created_at=models.DateTimeField(default=timezone.now)
    is_used=models.BooleanField(default=False)
    

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=3)