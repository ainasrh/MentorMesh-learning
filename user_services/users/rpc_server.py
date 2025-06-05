import pika
import json
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_services.settings")
django.setup()

from users.models import User  # adjust import to your model

RABBITMQ_HOST = 'rabbitmq'  # or use from settings/env
TRAINER_QUEUE = 'trainer_queue'

def get_trainer_data(trainer_id):
    try:
        trainer = User.objects.get(id=trainer_id,role='trainer')
        return {
            "id": trainer.id,
            "name": trainer.name,
            "email": trainer.email
        }
    except User.DoesNotExist:
        return {"error": "Trainer not found"}

def on_request(ch, method, props, body):
    print("📩 Received a message from course_service:", body)
    data = json.loads(body)
    trainer_id = data.get("trainer_id")
    response = get_trainer_data(trainer_id)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=TRAINER_QUEUE)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=TRAINER_QUEUE, on_message_callback=on_request)

    print(" [x] Awaiting RPC requests from course_service")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
