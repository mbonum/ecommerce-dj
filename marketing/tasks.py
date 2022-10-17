# from datetime import datetime, timedelta
# from django.conf import settings
# from django.core.mail import EmailMessage
# # from marketing.models import Uptime, Site
# from accounts.models import User


# if not Uptime.objects.filter(status='issue', site=site,
#                              date__gte=datetime.now() - timedelta(minutes=10)).exists():
#     EMAILS = [x.email for x in User.objects.all() if x.send_email_for_issues]
#     EMAIL = EmailMessage("We just had a time out",
#                          "Please check our website, we might have issues.",
#                          "https://status.armonia.world",
#                          settings.DEFAULT_FROM_EMAIL, [User.objects.first().email],
#                          [EMAILS], fail_silently=True)
#     EMAIL.send()

# Downtime
# if not Uptime.objects.filter(status='down', site=site,
#                              date__gte=datetime.now() - timedelta(minutes=10)).exists():
#     EMAILS = [x.email for x in User.objects.all() if x.send_email_for_downtime]
#     EMAIL = EmailMessage("A site has issues.",
#                          "Please check our website, we might have some serious problems.",
#                          "https://status.armonia.world",
#                          settings.DEFAULT_FROM_EMAIL, [User.objects.first().email],
#                          [EMAILS], fail_silently=True)
#     EMAIL.send()
