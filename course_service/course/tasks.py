# from celery import shared_task
# import time
# import logging

# logger=logging.getLogger(__name__)

# @shared_task
# def send_enrollment_email(user_id, course_id):
#     # Replace with actual email logic later
#     logger.info(f"📨 Sending enrollment confirmation to user {user_id} for course {course_id}...")
#     time.sleep(2)
#     logger.info(f"✅ Email sent to user {user_id} for course {course_id}")