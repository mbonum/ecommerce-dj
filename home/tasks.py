from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger

from .emails import send_contact_email

# import sys

# from django.core.management import call_command


logger = get_task_logger(__name__)


@shared_task(name="send_contact_email_task")
def send_email_task(first_name, email, subject, text_area):
    logger.info("Sent contact form email")
    return send_contact_email(first_name, email, subject, text_area)
    # kwargs.get("message_type"),**kwargs
    # kwargs.get("first_name"),
    # kwargs.get("last_name"),
    # kwargs.get("email"),
    # kwargs.get("subject"),
    # kwargs.get("text_area"),
    # kwargs.get("postal_code"),


# @shared_task
# def add(x, y):
#     return x + y


# @shared_task
# def bkup():
#     sys.stdout = open("db.json", "w")
#     call_command("dumpdata", "home")


# celery -A core worker -l info
