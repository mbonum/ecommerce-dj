from django import forms

# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from .models import MarketingPreference


class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(
        label="Would you like to receive Armonia's Newsletter?",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "align-middle shadow focus:outline-none ml-2"}
        ),
    )

    class Meta:
        model = MarketingPreference
        fields = ("subscribed",)

    #     exclude = []
    #     widget = {
    #         'subscribed': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-primary")
    #         }
