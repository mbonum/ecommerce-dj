from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class MessageType(models.TextChoices):
    COLLABORATION = "C", _("Collaboration")
    EMPLOYMENT = "J", _("Employment")
    FEEDBACK = "F", _("Feedback")
    MISC = "M", _("Misc")


class Contact(models.Model):
    message_type = models.CharField(
        max_length=255, choices=MessageType.choices, default=MessageType.COLLABORATION
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    text = HTMLField(blank=True, null=True)
    postal_code = models.CharField(max_length=19, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    # confirm = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "email", "subject", "text", "postal_code"]

    # objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = _("Contacts")


class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_added",)
