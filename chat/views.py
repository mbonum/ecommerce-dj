# from django.http import JsonResponse
# from django.views import View
# from django.views.generic import TemplateView
from core.utils import random_string_generator
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls.base import reverse

from .forms import ChatForm, ContactForm
from .models import Message


def contact(request):
    if request.user.is_authenticated:
        form = ChatForm(request.POST or None)
    else:
        form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if request.user.is_authenticated:
                # The form doesn't ask the name
                e = request.user.email
                # Remove email domain
                name = e[: e.index("@")]
            else:
                name = request.POST.get("first_name")
            room = name + "-" + random_string_generator(8)
            msg = str(request.POST.get("text"))  # request.POST.get("topic") + "\n" +
            # form Meta fields
            message = Message.objects.get_or_create(username=name, room=room, text=msg)
            return redirect(reverse("chat:room", args=[str(room)]) + f"?user={name}")
        # kwargs={}
        # return render(
        #     request,
        #     "chat/room.html",
        #     {"room": room, "user": name, "texts": message},
        # )

        # send automatic email with chatroom link

    return render(request, "chat/contact.html", {"form": form})


def room(request, room):
    usr = (
        request.GET.get("user") if request.GET.get("user") else room[: room.index("-")]
    )
    msg = Message.objects.filter(room=room)[0:25]
    return render(
        request,
        "chat/room.html",
        {"user": usr, "room": room, "texts": msg},
    )


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
#     subject = _("Thank you for contacting us") # + getattr(settings, "ENV_NAME", "Clavem")
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
#     # msg = _("Thank you for contacting us. We will answer you as soon as humanly possible.")
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


# def contact_page(request):
#     # docs.djangoproject.com/en/3.2/topics/email
#     form_class = ContactForm(request.POST or None)

#     if form_class.is_valid():
#         if request.accepts("application/json"):
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
#         if request.accepts("application/json"):
#             return HttpResponse(errors, status=400, content_type="application/json")

#     content = {
#         "form": form_class,
#     }
#     return render(request, "home/contact.html", content)