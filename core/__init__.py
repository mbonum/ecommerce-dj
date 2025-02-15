# https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
# Ensure the app is always imported
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ("celery_app",)
