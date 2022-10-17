from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Contact, MessageType

# from tinymce.widgets import TinyMCE # https://django-tinymce.readthedocs.io/en/latest/usage.html?highlight=attrs

# from .tasks import send_email_task

USER = get_user_model()


class ContactForm(forms.Form):
    message_type = forms.ChoiceField(
        label=_("Why are you writing us?"),
        required=True,
        choices=MessageType.choices,
        widget=forms.Select(
            attrs={
                "id": "messagetype",
                "class": "flex w-full appearance-none border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    first_name = forms.CharField(
        label=_("First name"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "contact_firstname",
                "placeholder": _("First name"),
                "class": "flex border border-gray-300 focus:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "contact_lastname",
                "placeholder": _("Last name"),
                "class": "flex border border-gray-300 focus:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
                "type": "text",
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "id": "contact_email",
                "placeholder": _("Email"),
                "class": "flex border border-gray-300 focus:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
                "type": "text",
            }
        ),
    )
    subject = forms.CharField(
        label=_("Topic"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "contact_subject",
                "placeholder": _("Topic"),
                "class": "flex w-full border border-gray-300 focus:border-yellow-500 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
                "spellcheck": "true",
            }
        ),
    )
    text = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(  # widget=TinyMCE(attrs={'cols': 80, 'rows': 30, 'textarea':  "Everyone knows something someone else doesn't."})
            attrs={
                "id": "contact_text",
                "placeholder": _("Clear and concise."),
                "class": "flex w-full hover:border-yellow-600 border border-gray-500 rounded-lg text-black placeholder-gray-800 shadow hover:shadow-md focus:outline-none focus:ring-2 ring-yellow-200 ring-offset-transparent ring-offset-2 py-1 px-2",
                "spellcheck": "true",
            }
        ),  #'cols': 80, 'rows': 40,
    )
    postal_code = forms.CharField(
        label=_("Postal code"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "contact_pc",
                "placeholder": _("Postal code"),
                "class": "border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )

    class Meta:
        model = Contact
        fields = (
            "message_type",
            "first_name",
            "last_name",
            "email",
            "subject",
            "text",
            "postal_code",
        )

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
