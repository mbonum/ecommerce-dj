"""/cart/checkout/"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Address, AddressType

# border border-gray-300 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2 mb-3 rounded-lg shadow placeholder-gray-900
class AddressForm(forms.ModelForm):
    address_type = forms.ChoiceField(
        choices=AddressType.choices,
        widget=forms.Select(
            attrs={
                "id": "id_address_type",
                "class": "rounded-lg shadow appearance-none w-full border border-gray-300 focus:border-yellow-500 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 px-2 py-1",
            }
        ),
    )
    street = forms.CharField(
        label=_("Street address or post office box"),
        widget=forms.TextInput(
            attrs={
                "id": "id_street",
                # "placeholder": "3 Main St.",
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    city = forms.CharField(
        label=_("City"),
        widget=forms.TextInput(
            attrs={
                "id": "id_city",
                # "placeholder": _("City"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
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
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    country = forms.CharField(
        label=_("Country"),
        widget=forms.TextInput(
            attrs={
                "id": "id_country",
                # "placeholder": _("Country"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    postal_code = forms.CharField(
        label=_("Postal code / Zip"),
        widget=forms.TextInput(
            attrs={
                "id": "id_zip",
                # "placeholder": _("Postal code"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
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
