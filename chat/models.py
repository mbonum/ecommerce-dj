from django.db import models
from django.utils.translation import gettext_lazy as _

# from tinymce.models import HTMLField


class MsgType(models.TextChoices):
    COLLABORATION = "C", _("Collaboration")
    JOB = "J", _("Job")
    FEEDBACK = "F", _("Feedback")
    SUPPORT = "S", _("Support")
    # MISC = "M", _("Misc")


class Contact(models.Model):
    message_type = models.CharField(
        max_length=255, choices=MsgType.choices, default=MsgType.COLLABORATION
    )  # tag msg for support team
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    topic = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)  # HTMLField
    # postal_code = models.CharField(max_length=19, blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    # confirm = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "email", "topic", "text"]  # , "postal_code"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = _("Contacts")


# class MessageManager(models.Manager):get_or_create
#     def new_or_get(self, request):
#         room = request.session.get("room", None)
#         qs = self.get_queryset().filter(room=room)
#         if qs.count() == 1:
#             new = False
#             message = qs.first()
#             message.save()
#         else:
#             user = request.session.get("username", None)
#             message = Message.objects.new(username=user)
#             new = True
#             request.session["message"] = message.id
#         return message, new

# user = request.user
# obj = None
# created = False
# if user.is_authenticated:
#     obj, created = self.model.objects.get_or_create(user=user, email=user.email)
# else:
#     pass
# return obj, created


class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)  # HTMLField()
    sent = models.DateTimeField(auto_now_add=True)

    # objects = MessageManager()

    class Meta:
        ordering = ["sent"]
