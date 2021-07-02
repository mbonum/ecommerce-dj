from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from .models import MarketingPreference


class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(
        label=_(f"Would you like to receive {settings.ENV_NAME} newsletter?"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "id": "id_subscribed",
                "class": "cursor-pointer shadow transform hover:scale-110 focus:outline-none",
            }
        ),
    )

    class Meta:
        model = MarketingPreference
        fields = ("subscribed",)

    #     exclude = []
    #     widget = {
    #         'subscribed': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-primary")
    #         }
