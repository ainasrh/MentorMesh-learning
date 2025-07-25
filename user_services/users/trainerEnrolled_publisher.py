import pika
import uuid
import json
import os
import threading

from dotenv import load_dotenv
load_dotenv()

def get_enrolled_details(trainer_id):
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host= os.getenv("RABBITMQ_HOST",'rabbitmq'),
            credentials=pika.PlainCredentials(
                os.getenv("RABBITMQ_DEFAULT_USER","user"),
                os.getenv("RABBITMQ_DEFAULT_PASS","password")
            )
        )
    )
    channel = connection.channel()

    result = channel.queue_declare(queue="", exclusive=True)
    callback_queue = result.method.queue

    correlation_id = str(uuid.uuid4())
    response_data = {}

    def on_response(ch, method, properties, body):  
        if correlation_id == properties.correlation_id:
            nonlocal response_data
            response_data = json.loads(body)
            ch.stop_consuming()

    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

    timeout_seconds = 10
    timer = threading.Timer(timeout_seconds, channel.stop_consuming)
    timer.start()


    channel.basic_publish(
        exchange='',
        routing_key='enrolled_que',
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=correlation_id
        ),
        body=json.dumps({"trainer_id": trainer_id})
    )

    print(f"⏳ Sent request for user {trainer_id}, waiting for reply...")

    channel.start_consuming()
    connection.close()

    return response_data
