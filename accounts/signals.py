"""
https://docs.djangoproject.com/en/4.1/topics/signals/
"""
from django.dispatch import Signal

USER_LOGGED_IN = Signal()  # providing_args=["instance", "request"]
