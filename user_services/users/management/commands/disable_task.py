from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask

class Command(BaseCommand):
    help = "Disable a periodic task by name"

    def handle(self, *args, **kwargs):
        try:
            task = PeriodicTask.objects.get(name="Print time task")
            task.enabled = False
            task.save()
            self.stdout.write(self.style.SUCCESS("✅ Task disabled successfully."))
        except PeriodicTask.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Task not found."))
    