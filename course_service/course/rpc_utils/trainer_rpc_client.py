import pika
import uuid
import json
import time


RABBITMQ_HOST = 'rabbitmq'  # or use from settings/env
TRAINER_QUEUE = 'trainer_queue'

class TrainerRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        print("📩 Received reply from user_service:", body)
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, trainer_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key=TRAINER_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps({"trainer_id": trainer_id})
        )

        print("📤 Sent request to user_service")

        while self.response is None:
            self.connection.process_data_events(time_limit=5)

        return self.response