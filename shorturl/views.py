from analytics.models import ClickEvent
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

# from django.http import HttpResponseRedirect # Http404
from django.shortcuts import redirect, render  # , get_object_or_404

# from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from .forms import SubmitURLForm
from .models import ClUrl


class ShortURLView(LoginRequiredMixin, View):
    # permission_denied_message = _("You are not allowed here.")
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_admin or not request.user.is_staff:
                raise PermissionDenied
        else:
            raise PermissionDenied
        form = SubmitURLForm
        context = {"title": "CLVM URL Shortener", "form": form}
        return render(request, "shorturl/shorturl.html", context)

    def post(self, request, *args, **kwargs):
        form = SubmitURLForm(request.POST)
        context = {"title": "CLVM URL shortener", "form": form}
        template = "shorturl/shorturl.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = ClUrl.objects.get_or_create(url=new_url)
            # context = {"object": obj, "created": created}
            if created:
                context = {
                    "title": _("Short URL created"),
                    "object": obj,
                    "created": created,
                }
                template = "shorturl/shorturl-done.html"
            else:
                context = {"title": _("Short URL exists"), "object": obj}
                template = "shorturl/shorturl-exists.html"
        return render(request, template, context)


class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        # obj = get_object_or_404(ClUrl, shortcode=shortcode)
        qs = ClUrl.objects.filter(shortcode=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return redirect(obj.url)  # HttpResponseRedirect
