from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,TrainerProfile

# this for same time multiple user change their role it will store based on their id

old_roles={}

# before saving it will check that user is already exist or not if exist it will store that  user role in in a dictionary based on the user id
@receiver(pre_save,sender=User)
def track_old_role(sender,instance,**kwargs):
    if instance.pk:
        try:
            old_user = User.objects.get(pk=instance.id)
            # store old role based o
            old_roles[instance.id] = old_user.role
        except User.DoesNotExist:
            old_roles[instance.id] = None
            

@receiver(post_save,sender=User)
def create_trainer_profile(sender,instance,created,**kwargs):
    old_role = old_roles.pop(instance.pk,None)

    if created and instance.role == "trainer":
        TrainerProfile.objects.create(user=instance)
    
    #check is that old role not= trainer and new role is ="trainer " then it will create a new trainer profile in here  
    elif not created and old_role != "trainer" and instance.role == "trainer":
        if not hasattr(instance,'trainer_profile'):
            TrainerProfile.objects.create(user=instance)    
