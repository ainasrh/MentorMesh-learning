import pika, json, os
from decouple import config

RABBITMQ_HOST = config("RABBITMQ_HOST", default="rabbitmq")
QUEUE_NAME = "course_enrollment_queue"

def publish_payment_success(user_id, course_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    payload = {
        "user_id": user_id,
        "course_id": course_id
    }

    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
