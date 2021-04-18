from __future__ import absolute_import, unicode_literals

# from celery import shared_task
from celery.utils.log import get_task_logger
from core.celery import app

from .emails import send_contact_email

logger = get_task_logger(__name__)


@app.task(name="send_email_task")
def send_email_task(**kwargs):
    logger.info("Sent contact form email")
    return send_contact_email(
        kwargs.get("message_type"),
        kwargs.get("first_name"),
        kwargs.get("last_name"),
        kwargs.get("email"),
        kwargs.get("subject"),
        kwargs.get("text_area"),
        kwargs.get("postal_code")
    )


# @shared_task
# def add(x, y):
#     return x + y

# celery -A core worker -l info
