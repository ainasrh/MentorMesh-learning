from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from datetime import timedelta

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(username,email):
    logger.info(f"✅ Email sent to {email}")
    subject = "Welcome Message"
    message = f"Welcome To MentoMesh {username}"
    send_mail(subject,message,settings.EMAIL_HOST_USER,[email])
    logger.info(f"📨 Task started for user ID {username}")


# Debug The celery Beat

# @shared_task
# def print_current_time():
#     print(f"[⏰] Current time is: {now()}")

# @shared_task
# def print_without_admin():
#     print(f"[⏰] Current time  without admin working: {now()}")

@shared_task
def daily_mail():
    # send mail daily learners logged users 
    User=get_user_model()
    recent_time = now() - timedelta(hours=24)

    active_users=User.objects.filter(role="learner")
    for user in active_users:
        logger.info("daily email worked")
        subject="Morning Message"
        message=f"Good Morning {user.username} Bless You Have A good Day From MentorMesh"
        send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email],fail_silently=False,)
