from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Contact, MessageType

# from tinymce.widgets import TinyMCE # https://django-tinymce.readthedocs.io/en/latest/usage.html?highlight=attrs

from .tasks import send_email_task

USER = get_user_model()


class ContactForm(forms.Form):
    message_type = forms.ChoiceField(
        required=True,
        choices=MessageType.choices,
        widget=forms.Select(
            attrs={
                "id": "message-type-id",
                "class": "font-c-sans rounded appearance-none w-full border border-gray-400 text-black py-2 px-2 pr-8 leading-tight outline-none bg-white focus:ring-2 focus:ring-yellow-100 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    first_name = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "name": "first_name",
                "id": "contact-first-name",
                "placeholder": _("First name"),
                "class": "font-c-sans rounded focus:ring-2 focus:ring-yellow-100 focus:ring-offset-transparent focus:ring-offset-2 appearance-none w-full text-black border border-gray-400 py-2 px-3 focus:outline-none focus:bg-white placeholder-black",
                "type": "text",
            }
        ),
    )
    last_name = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "name": "last_name",
                "id": "contact-last-name",
                "placeholder": _("Last name"),
                "class": "font-c-sans rounded focus:ring-2 focus:ring-yellow-100 focus:ring-offset-transparent focus:ring-offset-2 appearance-none w-full text-black border border-gray-400 py-2 px-3 focus:outline-none focus:bg-white placeholder-opacity-100 placeholder-black",
                "type": "text",
            }
        ),
    )
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "name": "email",
                "id": "contact-email",
                "placeholder": "Email",
                "class": "font-c-sans rounded focus:ring-2 focus:ring-yellow-100 focus:ring-offset-transparent focus:ring-offset-2 appearance-none w-full bg-white text-black border border-gray-400 py-2 px-3 focus:outline-none focus:bg-white placeholder-black",
                "type": "text",
            }
        ),
    )
    subject = forms.EmailField(
        label="",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "name": "subject",
                "id": "contact-subject",
                "placeholder": _("Subject"),
                "class": "font-c-sans rounded focus:ring-2 focus:ring-yellow-100 focus:ring-offset-transparent focus:ring-offset-2 appearance-none w-full bg-white text-black border border-gray-400 py-2 px-3 focus:outline-none focus:bg-white placeholder-black",
                "type": "text",
            }
        ),
    )
    textarea = forms.CharField(
        label="",
        required=True,
        widget=forms.Textarea(  # widget=TinyMCE(attrs={'cols': 80, 'rows': 30, 'textarea':  "Everyone knows something someone else doesn't."})
            attrs={
                "name": "textarea",
                "id": "contact-textarea",
                "placeholder": _("Clear and concise."),
                "class": "font-c-sans rounded focus:ring-2 focus:ring-yellow-100 focus:ring-offset-transparent focus:ring-offset-2 w-full h-40 tracking-wide border border-gray-400 text-black py-2 px-3 placeholder-gray-800 hover:shadow",
            }
        ),  #'cols': 80, 'rows': 40,
    )
    postal_code = forms.EmailField(
        label="",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "name": "email",
                "id": "contact-postal-code",
                "placeholder": _("Postal code"),
                "class": "rounded focus:ring-2 focus:ring-yellow-100 focus:ring-offset-transparent focus:ring-offset-2 appearance-none block w-full bg-white text-black border border-gray-400 py-2 px-3 leading-tight focus:outline-none focus:bg-white placeholder-gray-900 hover:shadow",
                "type": "text",
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
            "textarea",
            "postal_code",
        )

    def send_email(self):
        print("*****", self.cleaned_data["first_name"])
        send_email_task.delay(
            self.cleaned_data["message_type"],
            self.cleaned_data["first_name"],
            self.cleaned_data["last_name"],
            self.cleaned_data["email"],
            self.cleaned_data["subject"],
            self.cleaned_data["textarea"],
            self.cleaned_data["postal_code"],
        )
