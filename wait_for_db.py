import os
import django
import pytz

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartForm.settings")
django.setup()

from django.db.models import Q
from smart_emailApp.models import EmailTask, ErrorReport
from scheduler.send_email import buildEmail
from datetime import datetime


# Define your function here
def check_for_task():
    # Get the current time in UTC
    now_utc = datetime.now(pytz.utc)

    # Convert UTC time to Eastern Standard Time (EST)
    eastern = pytz.timezone('US/Eastern')
    now = now_utc.astimezone(eastern)

    # Print the EST time in a specific format
    print(now.strftime('%Y-%m-%d %H:%M:%S %Z'))
    print(now)

    emailtasks = EmailTask.objects.filter(Q(status='Not Scheduled') | Q(status='Scheduled'))

    for emailtask in emailtasks:
        if emailtask.status in ["Not Scheduled", "Scheduled"]:
            try:
                # check if the email has already been sent today
                if emailtask.last_sent_date and emailtask.last_sent_date == now.date():
                    print("Email has already been sent today, skipping...")
                    continue

                print(emailtask)

                print(f"###########  Email ID of the email to send  " + str(emailtask.emailToSend))

                if (buildEmail(emailtask.id, emailtask.emailToSend.id)):
                    err = ErrorReport(name=emailtask.task_name, decription=f'{emailtask.task_name} sent at {now}')
                    emailtask.last_sent_date = now.date()
                else:
                    err = ErrorReport(name=f'{emailtask.task_name} Not Sent',
                                      decription=f'{emailtask.task_name} Not sent at {now}')

                emailtasks.update(status="Scheduled")
                # update the last sent date to today's date
                emailtask.save()

            except:
                if emailtask.date_to_sending <= now:
                    print("Expired")
                    emailtasks.update(status="Expired")
                    print("Changed to Expired")
                    return emailtask.id
                else:
                    print("Nothing to run###")


check_for_task()