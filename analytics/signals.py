from django.dispatch import Signal

OBJECT_VIEWED_SIGNAL = Signal()  # providing_args=["instance", "request"]
