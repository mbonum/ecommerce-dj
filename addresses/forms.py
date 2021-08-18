"""/cart/checkout/"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Address, AddressType


class AddressForm(forms.ModelForm):
    address_type = forms.ChoiceField(
        choices=AddressType.choices,
        widget=forms.Select(
            attrs={
                "id": "id_address_type",
                "class": "appearance-none bg-white form",
            }
        ),
    )
    street = forms.CharField(
        label=_("Street address"),  # / post office box
        widget=forms.TextInput(
            attrs={
                "id": "id_street",
                # "placeholder": "3 Main St.",
                "class": "form",
            }
        ),
    )
    city = forms.CharField(
        label=_("City"),
        widget=forms.TextInput(
            attrs={
                "id": "id_city",
                # "placeholder": _("City"),
                "class": "form",
            }
        ),
    )
    state = forms.CharField(
        label=_("Province / Region / State"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "id_state",
                # "placeholder": _("State"),
                "class": "form",
            }
        ),
    )
    country = forms.CharField(
        label=_("Country"),
        widget=forms.TextInput(
            attrs={
                "id": "id_country",
                # "placeholder": _("Country"),
                "class": "form",
            }
        ),
    )
    postal_code = forms.CharField(
        label=_("Postal code / Zip"),
        widget=forms.TextInput(
            attrs={
                "id": "id_zip",
                # "placeholder": _("Postal code"),
                "class": "form",
            }
        ),
    )

    class Meta:
        model = Address
        fields = (
            "street",
            "city",
            "state",
            "country",
            "postal_code",
        )  # "billing_profile", 'address_type', 'address_line_1', 'line_2',
