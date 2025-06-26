import json
import os
import sys
import django
import pika
import logging

from dotenv import load_dotenv
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_service.settings")

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from course.models import Enrollment


def process_message(ch, method, properties, body):
    try:
        user_request = json.loads(body)
        trainer_id = user_request.get("trainer_id")

        logger.info(f"📩 Received request for user ID: {trainer_id}")

        enroll_data = {"error": "No enrollments found"}
                                            # get trainer from foreign key table field table
        enroll_details = Enrollment.objects.filter(course__trainer=trainer_id)
        logger.info(f"enroll{enroll_details}")
        if not enroll_details.exists():
            enroll_data={"error":"No Erllments found"}
        else:
            enroll_data=[
                {
                    "user_id":enroll.user,
                    "course_id":enroll.course.id
                }
                for enroll in enroll_details
            ]

        

        response = json.dumps(enroll_data)

        if properties.reply_to:
            ch.basic_publish(
                exchange="",
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=response,
            )
            logger.info(f" Sent response to queue {properties.reply_to}")
        else:
            logger.warning("No reply_to property in request")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        logger.error("Failed to decode JSON from request")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.exception(f"Error while processing message: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="rabbitmq",
                credentials=pika.PlainCredentials(
                    os.getenv("RABBITMQ_DEFAULT_USER","user"),
                    os.getenv("RABBITMQ_DEFAULT_PASS","password")
                )
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue="enrolled_que", durable=True)

        logger.info(" Connected to RabbitMQ and waiting for messages...")
        channel.basic_consume(queue="enrolled_que", on_message_callback=process_message)
        channel.start_consuming()

    except pika.exceptions.ProbableAuthenticationError:
        logger.critical(" Authentication failed: Check RabbitMQ username/password")
    except pika.exceptions.AMQPConnectionError as e:
        logger.critical(f" Could not connect to RabbitMQ: {e}")
    except KeyboardInterrupt:
        logger.info(" Stopping consumer by user request...")
        try:
            connection.close()
        except:
            pass
    except Exception as e:
        logger.exception(f" Unexpected error occurred: {e}")


if __name__ == "__main__":
    start_consumer()
