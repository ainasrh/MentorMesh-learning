
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','user_services.settings')

app = Celery('user_service')

# - namespace='CELERY' means all celery-related configuration keys
app.config_from_object('django.conf:settings',namespace='CELERY')


# Load task modules from all registered Django apps. it look all registered task in task.py
app.autodiscover_tasks()


# app.task(bind=True,ignore_result=True)
# def debug_task(self):
#     print('task worked')
#     print(f'Request: {self.request}')
