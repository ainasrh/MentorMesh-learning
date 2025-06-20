from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError


# Create your models here.


class User(AbstractUser): 
    Role_Choice=[
        ('learner',"Learner"),
        ('trainer',"Trainer"),
        ('admin',"Admin")
    ]

    date_joined=None

    role=models.CharField(max_length=155,choices=Role_Choice,default="learner")
    avatar=models.ImageField(upload_to='avatars/',null=True,blank=True,default='avatars/default_avatar.jpg')
    bio=models.TextField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now=True)
    email=models.EmailField(unique=True)
    is_email_verified=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username'] 

class TrainerProfile(models.Model):
                                                                                                # opposit Relation from TrainerProfile to User model
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="trainer_profile",limit_choices_to={"role":"trainer"}) 
    experience = models.PositiveIntegerField(help_text="Experience in Years ", null=True,blank=True)
    qualification = models.CharField(max_length=255,null=True,blank=True)
    skills = models.TextField(null=True,blank=True)

    def clean(self):
        if self.user.role != "trainer":
            raise ValidationError("Only Trainer Can Create Trainer Profile")
        if self.experience is not None and self.experience > 50 :
            raise ValidationError('Experience cannot exeed 50 years')
        
    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)
    
    def __str__(self):
        return f" {self.user.email}  Trainer Profile"

class PasswordResetOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp_code =models.CharField(max_length=6)
    created_at=models.DateTimeField(default=timezone.now)
    is_used=models.BooleanField(default=False)
    

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=3)