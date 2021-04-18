# from django.template import Context#fn, ln, s, t, pc
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


def send_contact_email(**kwargs):
    context = {
        # "message_type": kwargs.get("message_type"),
        "first_name": kwargs.get("first_name"),
        # "last_name": kwargs.get("last_name" or None),
        "email": kwargs.get("email"),
        # "subject": kwargs.get("subject"),
        # "textarea": kwargs.get("textarea"),
        # "postal_code": kwargs.get("postal_code"),
    }
    subject = _("Thank you for contacting ") + getattr(settings, "ENV_NAME", "Clavem")
    body = render_to_string("email_msg.txt", context)
    email = EmailMessage(
        subject,
        body,
        getattr(settings, "DEFAULT_FROM_EMAIL", "support@clavem.co"),
        [
            kwargs.get("email"),
        ],
    )
    return email.send(fail_silently=False)
