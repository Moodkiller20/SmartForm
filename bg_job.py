import os
import django
from django.db.models.signals import post_save

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartForm.settings")

# initialize Django
django.setup()
from django.dispatch import receiver

from django.db.models import Q
# import your Django models and components here
from smart_emailApp.models import Emails, EmailTask, ErrorReport
from smart_emailApp.models import Emails, EmailTask, MyJobModel, Link
from datetime import datetime
import pytz
from scheduler.send_email import buildEmail





# def check_for_task():
#
#     # Get the current time in UTC
#     now_utc = datetime.now(pytz.utc)
#
#     # Convert UTC time to Eastern Standard Time (EST)
#     eastern = pytz.timezone('US/Eastern')
#     now = now_utc.astimezone(eastern)
#
#     # Print the EST time in a specific format
#     print(now.strftime('%Y-%m-%d %H:%M:%S %Z'))
#     print(now)
#
#
#     emailtasks = EmailTask.objects.filter(Q(status='Not Scheduled') | Q(status='Scheduled'))
#
#
#     for emailtask in emailtasks:
#         if emailtask.status in ["Not Scheduled", "Scheduled"]:
#             try:
#                 #email = EmailTask.objects.filter()
#                 print(emailtask)
#                 task_name =emailtask.task_name
#                 occurence = emailtask.task_occurence
#                 run_from = emailtask.date_from
#                 run_to = emailtask.date_to_sending
#                 print(f"###########  Email ID of the email to send  "+str(emailtask.emailToSend))
#
#                 buildEmail(emailtask.id, emailtask.emailToSend.id, )
#
#                 emailtasks.update(status="Scheduled")
#                 print("Changed to Scheduled")
#                 return emailtask.id
#             except:
#                 print("Error in 'check_for_task'function ")
#                 pass
#
#         if emailtask.date_to_sending <= now:
#             print("Expired")
#             emailtasks.update(status="Expired")
#             print("Changed to Expired")
#             return emailtask.id
#         else:
#             print("Nothing to run###")




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
                task_name = emailtask.task_name
                # occurence = emailtask.task_occurence
                # run_from = emailtask.date_from
                # run_to = emailtask.date_to_sending
                print(f"###########  Email ID of the email to send  "+str(emailtask.emailToSend))

                buildEmail(emailtask.id, emailtask.emailToSend.id)
                # Save the job details to the database
                my_job = MyJobModel(name=task_name, decription = "ran on"+str(now))
                my_job.save()
                print("Task saved")

                # update the last sent date to today's date
                emailtask.last_sent_date = now.date()
                emailtask.save()
            except:
                print("Error in 'check_for_task'function ")
                err = ErrorReport(name ="check_for_task",decription=" Error in check_for_task() in the bg_job.py")
                err.save()
                print("Error saved")

            if emailtask.date_to_sending <= now:
                print("Expired")
                emailtasks.update(status="Expired")
                print("Changed to Expired")
                return emailtask.id
            else:
                print("Nothing to run###")



check_for_task()
