"""
Email marketing
Using https://requestbin.fullcontact.com
POST method
data[email_type]: html
data[web_id]: 63774019
data[email]: mkb@gmail.com
data[merges][BIRTHDAY]:
data[ip_opt]: 151.62.165.32
type: unsubscribe
data[merges][LNAME]:
data[reason]: manual
data[merges][EMAIL]: mkb@gmail.com
data[merges][FNAME]:
data[merges][PHONE]:
data[list_id]: 19a203dae6
data[merges][ADDRESS]:
fired_at: 2018-11-29 15:54:29
data[id]: c4fe21552a
"""
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect  # , render
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, View

from .forms import MarketingPreferenceForm
from .mixins import CsrfExemptMixin
from .models import MarketingPreference
from .utils import Mailchimp

# from rest_framework import permissions
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from marketing.serializers import SubscriberSerializer

# https://us19.admin.mailchimp.com/lists/tools/webhooks-create?id=321186
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm()
    template_name = "marketing/change-email-form.html"
    success_url = "/settings/email/"
    success_message = _(
        "Your email preferences have been updated. Thank you!"
    )  # show on Save button

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/login/?next=/settings/email/")
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(
            *args, **kwargs
        )
        context["title"] = _("Email Preferences")
        return context

    def get_object(self):  # get_absolute_url is the default
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


class MailchimpWebhookView(CsrfExemptMixin, View):
    """
    https://us19.admin.mailchimp.com/lists/tools/webhooks-create?id=321186
    def get(self, request, *args, **kwargs):
        return HttpResponse('Thank You', status=200)
    """

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get("data[list_id]")
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get("data[email]")
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response["status"]
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                        subscribed=is_subbed,
                        mailchimp_subscribed=mailchimp_subbed,
                        mailchimp_msg=str(data),
                    )
        return HttpResponse(_("Thank You"), status=200)


#  def mail_chimp_webhook_view(request):
#     data = request.POST # usually it is a dictionary
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get('type')
#         email = data.get('data[email]')
#         response_status, response = Mailchimp().check_subscription_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == 'subscribed':
#             is_subbed, mailchimp_subbed = (True, True)
#         elif sub_status == 'unsubscribed':
#             is_subbed, mailchimp_subbed = (False, False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(
#                         subscribed=is_subbed,
#                         mailchimp_subscribed=mailchimp_subbed,
#                         mailchimp_msg=str(data))
#     return HttpResponse('Thank You', status=200)

# class SubscriberView(APIView):

#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):
#         serializer = SubscriberSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
