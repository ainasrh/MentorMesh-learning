import json
import os
import sys
import django
import pika
import logging
from course.tasks import send_enrollment_email

from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_service.settings")


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from course.models import Enrollment, Course  

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "course_enrollment_queue"

def enroll_user(user_id, course_id):
    try:
        course = Course.objects.get(id=course_id)
        Enrollment.objects.create(user=user_id, course=course)

        send_enrollment_email.delay(user_id, course_id)

        print(f"✅ Enrolled user {user_id} in course {course_id}")
    except Course.DoesNotExist:
        print(f" Course {course_id} not found")
    except Exception as e:
        print(f" Enrollment error: {e}")

def callback(ch, method, properties, body):
    print(f" Received: {body}")
    data = json.loads(body)
    enroll_user(data['user_id'], data['course_id'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print(" Course Service waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
