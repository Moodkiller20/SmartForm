import os
import django
import pytz
import logging

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartForm.settings")
django.setup()

from django.db.models import Q
from smart_emailApp.models import EmailTask, ErrorReport
from scheduler.send_email import buildEmail
from datetime import datetime





# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


# Define your function here
def check_for_task():
    # Get the current time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert UTC time to Eastern Standard Time (EST)
    eastern = pytz.timezone('US/Eastern')
    now = now_utc.astimezone(eastern)

    emailtasks = EmailTask.objects.filter(Q(status='Not Scheduled') | Q(status='Scheduled'))

    for emailtask in emailtasks:
        if emailtask.status in ["Not Scheduled", "Scheduled"]:
            try:
                # check if the email has already been sent today
                if emailtask.last_sent_date and emailtask.last_sent_date == now.date():
                    logging.info("Email has already been sent today, skipping...")
                    logging.info(f"Email Task ID: {emailtask.id}")
                    continue

                if buildEmail(emailtask.id, emailtask.emailToSend.id):
                    err = ErrorReport(name=emailtask.task_name, decription=f'{emailtask.task_name} sent at {now}')
                    logging.info("Email sent successfully.")
                    logging.info(f"Email Task ID: {emailtask.id}")
                    emailtask.last_sent_date = now.date()
                    emailtask.status = "Scheduled"
                    emailtask.save()
                else:
                    err = ErrorReport(name=f'{emailtask.task_name} Not Sent',
                                      decription=f'{emailtask.task_name} Not sent at {now}')
                    logging.error("Failed to send email.")
                    logging.error(f"Email Task ID: {emailtask.id}")

            except Exception as e:
                logging.exception(f"Error occurred while processing email task. Email Task ID: {emailtask.id}. Error: {str(e)}")

            finally:
                if emailtask.date_to_sending <= now:
                    emailtasks.update(status="Expired")
                    logging.info("Email task expired.")
                    logging.info(f"Email Task ID: {emailtask.id}")
                    return emailtask.id
                else:
                    logging.debug("Nothing to run###")


check_for_task()
