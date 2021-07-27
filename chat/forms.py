from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email

# from django.contrib.auth import get_user_model
# from tinymce.widgets import TinyMCE # https://django-tinymce.readthedocs.io/en/latest/usage.html?highlight=attrs

from .models import Contact, MsgType, Message

# from .tasks import send_email_task


class ContactForm(forms.Form):
    message_type = forms.ChoiceField(
        label=_("Why are you writing us?"),
        required=True,
        choices=MsgType.choices,
        widget=forms.Select(
            attrs={
                "id": "msgtype",
                "class": "flex w-full appearance-none bg-white border border-gray-300 focus:border-yellow-500 hover:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    first_name = forms.CharField(
        label=_("First name"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "chat_fn",
                # "placeholder": _("First name"),
                "class": "flex border border-gray-300 focus:border-yellow-500 hover:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "chat_ln",
                # "placeholder": _("Last name"),
                "class": "flex border border-gray-300 focus:border-yellow-500 hover:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
                "type": "text",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "chat_email",
                # "placeholder": _("Email"),
                "class": "flex border border-gray-300 focus:border-yellow-500 hover:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
                "autofocus": True,
            }
        ),
    )
    topic = forms.CharField(
        label=_("Topic"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "chat_topic",
                # "placeholder": _("Topic"),
                "class": "flex w-full border border-gray-300 focus:border-yellow-500 hover:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
                "spellcheck": "true",
            }
        ),
    )
    text = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(  # Clear and concise. widget=TinyMCE(attrs={'cols': 80, 'rows': 30, 'textarea':  "Everyone knows something someone else doesn't."})
            attrs={
                "id": "chat_text",
                # "placeholder": _("How can we help?"),"class": "",
                "rows": 4,
                "spellcheck": "true",
            }
        ),  #'cols': 80, 'rows': 40,
    )
    # postal_code = forms.IntegerField(
    #     label=_("Postal code"),
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             "id": "chat_pc",
    #             "placeholder": _("Postal code"),
    #             "class": "border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
    #         }
    #     ),
    # )

    class Meta:
        model = Contact
        fields = (
            "message_type",
            "first_name",
            "last_name",
            "email",
            "topic",
            "text",
            # "postal_code",
        )

    def clean_first_name(self):
        fn = self.cleaned_data["first_name"]
        cl = ["clavem", "clvm", "Clavem team"]
        if any(c in fn for c in cl):
            raise ValidationError(_("Name reserved."))
        return fn

    # def send_email(self):
    #     send_email_task.delay(
    #         self.cleaned_data["message_type"],
    #         self.cleaned_data["first_name"],
    #         self.cleaned_data["last_name"],
    #         self.cleaned_data["email"],
    #         self.cleaned_data["subject"],
    #         self.cleaned_data["text"],
    #         self.cleaned_data["postal_code"],
    #     )


class ChatForm(forms.Form):
    message_type = forms.ChoiceField(
        label=_("Why are you writing us?"),
        required=True,
        choices=MsgType.choices,
        widget=forms.Select(
            attrs={
                "id": "msgtype",
                "class": "flex w-full appearance-none bg-white border border-gray-300 focus:border-yellow-500 hover:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    topic = forms.CharField(
        label=_("Topic"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "chat_topic",
                # "placeholder": _("Topic"),
                "class": "flex w-full border border-gray-300 focus:border-yellow-500 hover:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
                "spellcheck": "true",
            }
        ),
    )
    text = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(
            attrs={
                "id": "chat_text",
                # "placeholder": _("How can we help?"),
                "class": "flex w-full focus:border-yellow-500 hover:border-yellow-500 border border-gray-400 rounded-lg placeholder-gray-800 shadow hover:shadow-md focus:outline-none focus:ring-2 ring-yellow-200 ring-offset-transparent ring-offset-2 py-1 px-2",
                "rows": 4,
                "spellcheck": "true",
            }
        ),
    )

    class Meta:
        model = Contact
        fields = (
            "message_type",
            "topic",
            "text",
        )


# class MessageForm(forms.Form):
#     text = forms.CharField(
#         label=_("Message"),
#         required=True,
#         widget=forms.Textarea(
#             attrs={
#                 "id": "chat_text",
#                 "placeholder": _("How can we help?"),
#                 "class": "flex w-full hover:border-yellow-600 border border-gray-400 rounded-lg placeholder-gray-800 shadow hover:shadow-md focus:outline-none focus:ring-2 ring-yellow-200 ring-offset-transparent ring-offset-2 py-1 px-2",
#                 "rows": 4,
#                 "spellcheck": "true",
#             }
#         ),
#     )

#     class Meta:
#         model = Message
#         fields = ("text",)
