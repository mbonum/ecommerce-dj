"""
https://docs.djangoproject.com/en/3.2/topics/signals/
"""
from django.dispatch import Signal

USER_LOGGED_IN = Signal(providing_args=["instance", "request"])
