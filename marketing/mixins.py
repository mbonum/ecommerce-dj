from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# marketing.views import MailchimpWebhookView


class CsrfExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)