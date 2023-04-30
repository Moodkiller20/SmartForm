import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from django.db.models.signals import post_save
from django.dispatch import receiver
from smart_emailApp.models import EmailTask




# Define your function here
def my_function():
    print("Email task saved with Scheduled status!")
