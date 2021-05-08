# import os
# from mimetypes import guess_type
# from wsgiref.util import FileWrapper
from core.utils import unique_slug_generator
from django.conf import settings

# from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse  # , JsonResponse#Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView  # FormView
from django.views.generic.edit import FormView  # get_language, activate

from .forms import ContactForm
from .models import Contact, Cookie, Donate, Message, Page, Privacy, Terms, Trademark

# from core.utils import render_to_pdf


# from subscribe.forms import JoinForm


class HomeView(SuccessMessageMixin, CreateView):
    template_name = "home/home.html"
    model = Page
    fields = "__all__"
    success_url = "/"

    def get_queryset(self):
        return Page.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["page_obj"] = HomeView.get_queryset(self)
        return context


# def home(request):
#     # Test internationalization
#     trans = translate(lang='de')
#     return(request, 'home.html', {'trans': trans})

# def translate(lang):
#     cur_lang = get_language()
#     try:
#         activate(lang)
#     finally:
#         activate(cur_lang)


class ContactView(FormView):
    template_name = "home/contact.html"
    form_class = ContactForm

    def form_valid(self, form):
        # form.send_email() # celery, rabbitmq docs
        fn = self.cleaned_data["first_name"]
        e = self.cleaned_data["email"]
        context = {
            # "message_type": kwargs.get("message_type"),
            "first_name": fn,
            # "last_name": kwargs.get("last_name" or None),
            "email": e,
            # "subject": self.cleaned_data["subject"],
            # "textarea": self.cleaned_data["textarea"],
            # "postal_code": kwargs.get("postal_code"),
        }
        subject = "Thank you for contacting " + getattr(settings, "ENV_NAME", "Clavem")
        body = render_to_string("email_msg.txt", context)
        email = EmailMessage(
            subject,
            body,
            getattr(settings, EMAIL_HOST_USER, "support@clavem.co"),
            [e],
            # reply_to=[kwargs.get("email")],
            headers={"Message-ID": make_msgid()},
        )
        email.send(fail_silently=False)
        # msg = "Thank you for contacting us. We will answer you as soon as humanly possible."
        return render(
            request,
            "home/room.html",
            {
                "room": unique_slug_generator(fn),
                "username": unique_slug_generator(fn),
                "messages": self.cleaned_data["textarea"],
            },
        )
        # render(request, "carts/checkout-done.html", {})


def room(request, room):
    # name =   #"You" request.GET.get("username", "You")
    messages = Message.objects.filter(room=room)[0:25]
    return render(
        request,
        "home/room.html",
        {"room": room, "messages": messages},  # "username": name,
    )


# def contact_page(request):
#     """docs.djangoproject.com/en/3.2/topics/email/"""
#     form_class = ContactForm(request.POST or None)

#     if form_class.is_valid():
#         if request.is_ajax():
#             return JsonResponse(
#                 {"message": _("We will answer you as soon as humanly possible.")}
#             )
#         subject = _("Contact Form") + form_class["first_name"] + form_class["last_name"]
#         message = form_class["message"]
#         from_email = form_class["email"]  # check email validity
#         to_list = getatts(settings, "EMAIL_HOST_USER", "")
#         send_mail(
#             subject, message, from_email, to_list, fail_silently=False
#         )  # setup automatic email
#     else:
#         return HttpResponse("Not valid", status=400, content_type="application/json")

#     if form_class.errors:
#         errors = form_class.errors.as_json()
#         if request.is_ajax():
#             return HttpResponse(errors, status=400, content_type="application/json")

#     content = {
#         "form": form_class,
#     }
#     return render(request, "home/contact.html", content)


class DonateView(CreateView):
    template_name = "home/donate.html"
    success_url = "/donate/"
    model = Donate
    fields = "__all__"

    def get_queryset(self):
        return Donate.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(DonateView, self).get_context_data(*args, **kwargs)
        context["text"] = DonateView.get_queryset(self)
        return context


class CookieView(CreateView):
    template_name = "home/policy.html"  #'policies/cookie.html'
    success_url = "/cookie/"
    model = Cookie
    fields = "__all__"

    def get_queryset(self):
        return Cookie.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(CookieView, self).get_context_data(*args, **kwargs)
        context["text"] = CookieView.get_queryset(self)
        # context['download'] = CookieView.get_download_url(self)
        return context

    # def get_download_url(self):
    #     fileroot = settings.MEDIA_ROOT
    #     filepath = self  # .url /media/cookie
    #     final_filepath = os.path.join(
    #         fileroot, filepath)  # where the file is stored
    #     with open(final_filepath, 'rb') as _f:
    #         wrapper = FileWrapper(_f)
    #         # content = 'some'
    #         mimetype = 'application/force-download'  # 'text/plain' for a txt file
    #         # look the extension of the first [0] file
    #         guessed_mimetype = guess_type(filepath)[0]
    #         if guessed_mimetype:
    #             mimetype = guessed_mimetype
    #         response = HttpResponse(wrapper, content_type=mimetype)  # content
    #         response["Content-Disposition"] = f'attachment;filename={self.pdf_name}'
    #         response["X-SendFile"] = str(self.pdf_name)
    #         return response


# def download(request, path):
# file_path = os.path.join(settings.MEDIA_ROOT, path)
# if os.path.exists(file_path):
#     with open(file_path, 'rb') as fh:
#         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#         return response
# raise Http404


class PrivacyView(CreateView):
    template_name = "home/policy.html"  #'policies/privacy.html'
    success_url = "/privacy/"
    model = Privacy
    fields = "__all__"

    def get_queryset(self):
        return Privacy.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(PrivacyView, self).get_context_data(*args, **kwargs)
        context["text"] = PrivacyView.get_queryset(self)
        return context


class TermsView(CreateView):
    template_name = "home/policy.html"
    success_url = "/terms/"
    model = Terms
    fields = "__all__"

    def get_queryset(self):
        return Terms.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(TermsView, self).get_context_data(*args, **kwargs)
        context["text"] = TermsView.get_queryset(self)
        return context


class TrademarkView(CreateView):
    template_name = "home/trademark.html"
    success_url = "/trademark/"
    model = Trademark
    fields = "__all__"

    def get_queryset(self):
        return Trademark.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(TrademarkView, self).get_context_data(*args, **kwargs)
        context["text"] = TrademarkView.get_queryset(self)
        return context


# def donate_page(request):
#     """Bitcoin donation (add other crypto currencies)"""
#     content = {
#         'title': 'Support Clavem',
#         'body': 'Our hope is to have one global stable cryptocurrency that ensures transparency.',
#         'address_btc': 'public key btc',
#         'address_eth': 'public key eth'  # create Clavem's cryptocurrency wallet code
#     }
#     return render(request, 'home/donate.html', content)
