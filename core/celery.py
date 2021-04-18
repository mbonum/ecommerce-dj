# https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django
# open new terminal and run: celery -A core worker -l info
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
#broker='amqp://',# RabbitMQ  amqp://localhost,
#  backend='rpc://',
#  include=['core.tasks'] , backend='redis://localhost', broker='pyamqp://')
# keep track of the tasks’ states in redis and use rabbitMQ as message broker

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")# gives RecursionError: maximum recursion depth exceeded

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
