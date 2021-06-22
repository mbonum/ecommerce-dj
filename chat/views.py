from django.conf import settings
from django.shortcuts import render

# from django.views import View
# from django.http import JsonResponse
# from django.views.generic import TemplateView
from .forms import ContactForm
from .models import Message


def contact(request):
    form_class = ContactForm  # (request.POST or None)

    # if form_class.is_valid():
    #     fn = form_class["first_name"]
    #     ln = form_class["last_name"]
    #     print("*** ", fn)
    # else:
    #     return HttpResponse("Not valid")
    return render(request, "chat/contact.html", {"form": form_class})


def room(request, room):
    name = request.GET.get("username", "Anonym")
    messages = Message.objects.filter(room=room)[0:25]
    return render(
        request,
        "chat/room.html",
        {"room": room, "username": name, "messages": messages},
    )


# class Success(TemplateView):
#     template_name = "chat/success.html"


# class Checkpage(TemplateView):
#     template_name = "chat/check.html"

#     def get_context_data(self, **kwargs):
#         # product = Product.objects.get(name="test")
#         context = super(Checkpage, self).get_context_data(**kwargs)
#         context.update({"STRIPE_PUB_KEY": settings.STRIPE_PUB_KEY})
#         return context

# class ContactView(FormView):
#     template_name = "home/contact.html"
#     form_class = ContactForm

# def form_valid(self, form):
#     # form.send_email() # celery, rabbitmq docs
#     fn = self.cleaned_data["first_name"]
#     e = self.cleaned_data["email"]
#     context = {
#         # "message_type": kwargs.get("message_type"),
#         "first_name": fn,
#         # "last_name": kwargs.get("last_name" or None),
#         "email": e,
#         # "subject": self.cleaned_data["subject"],
#         # "textarea": self.cleaned_data["textarea"],
#         # "postal_code": kwargs.get("postal_code"),
#     }
#     subject = "Thank you for contacting " + getattr(settings, "ENV_NAME", "Clavem")
#     body = render_to_string("email_msg.txt", context)
#     email = EmailMessage(
#         subject,
#         body,
#         getattr(settings, EMAIL_HOST_USER, "support@clavem.co"),
#         [e],
#         # reply_to=[kwargs.get("email")],
#         headers={"Message-ID": make_msgid()},
#     )
#     email.send(fail_silently=False)
#     # msg = "Thank you for contacting us. We will answer you as soon as humanly possible."
#     return render(
#         request,
#         "home/room.html",
#         {
#             "room": unique_slug_generator(fn),
#             "username": unique_slug_generator(fn),
#             "messages": self.cleaned_data["textarea"],
#         },
#     )
# render(request, "carts/checkout-done.html", {})


# def contact(request):
#     form_class = ContactForm  # (request.POST or None)

#     # if form_class.is_valid():
#     #     fn = form_class["first_name"]
#     #     ln = form_class["last_name"]
#     #     print("*** ", fn)
#     # else:
#     #     return HttpResponse("Not valid")
#     return render(request, "home/contact.html", {"form": form_class})


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
