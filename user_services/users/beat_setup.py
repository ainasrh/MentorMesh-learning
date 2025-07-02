
from django_celery_beat.models import PeriodicTask,IntervalSchedule
import json

def setup_periodic_tasks():
    # Get Or Create Interverl
    schedule,created = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.SECONDS,
    )


    # Create periodic Task If Not Created

    if not PeriodicTask.objects.filter(name="Print time task").exists():
        PeriodicTask.objects.create(
            interval=schedule, # Use Created Intervel
            name="Print time task",
            task="users.tasks.print_without_admin", # Full path Of the Task
            args=json.dumps([])

        )


def create_daily_mail_task():
    schedule,created = IntervalSchedule.objects.get_or_create(
        minute="0",
        hour="10",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
        timezone='Asia/Kolkata'
    )

    if not PeriodicTask.objects.filter(name="Send Daily Email at 10AM"):
        PeriodicTask.objects.create(
            interval=schedule,
            name="Send Daily Email at 10AM",
            task="users.tasks.dai   ly_mail",
            args=json.dumps([])
        )
        