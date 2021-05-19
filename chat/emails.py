# from django.template import Context
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

# EMAIL = getattr(settings, "EMAIL_HOST_USER", "support@clavem.co")#"mr.m.bonomi@gmail.com"
# PASSWORD = getattr(settings, "EMAIL_HOST_PASSWORD")#"qsjnlxpwoqwcceyr"


# def send_mail(
#     text="Email Body",
#     subject="Hello World",
#     from_email=EMAIL,
#     to_emails=None,
#     html=None,
# ):
#     assert isinstance(to_emails, list)
#     msg = MIMEMultipart("alternative")
#     msg["From"] = from_email
#     msg["To"] = ", ".join(to_emails)
#     msg["Subject"] = subject
#     txt_part = MIMEText(text, "plain")
#     msg.attach(txt_part)
#     if html != None:
#         html_part = MIMEText(html, "html")
#         msg.attach(html_part)
#     msg_str = msg.as_string()
#     # login to my smtp server
#     server = smtplib.SMTP(host="smtp.gmail.com", port=587)
#     server.ehlo()
#     server.starttls()
#     server.login(EMAIL, PASSWORD)
#     server.sendmail(from_email, to_emails, msg_str)
#     server.quit()
#     # with smtplib.SMTP() as server:
#     #     server.login()
#     #     pass


def send_contact_email(**kwargs):
    # print("**** ", kwargs.get("first_name"))first_name, email, subject, text
    email = kwargs.get("email")
    context = {
        # "message_type": kwargs.get("message_type"),
        "first_name": kwargs.get("first_name"),
        # "last_name": kwargs.get("last_name" or None),
        "email": email,
        "subject": kwargs.get("subject"),
        "textarea": kwargs.get("text"),
        # "postal_code": kwargs.get("postal_code"),
    }
    subject = _("Thank you for contacting " + getattr(settings, "ENV_NAME", "Clavem"))
    body = render_to_string("email_msg.txt", context)
    email = EmailMessage(
        subject,
        body,
        settings.EMAIL_HOST_USER,  # getattr(, "support@clavem.co"),
        [
            email,
        ],
        # reply_to=[email],
        # headers={"Message-ID": make_msgid()},
    )
    return email.send(fail_silently=False)


# 'Hello',
# 'Body goes here',
# 'from@example.com',
# ['to1@example.com', 'to2@example.com'],
# ['bcc@example.com'],
# reply_to=['another@example.com'],
# headers={'Message-ID': 'foo'},
