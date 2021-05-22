"""/cart/checkout/"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Address, AddressType

# border border-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2 mb-3 rounded-lg shadow placeholder-gray-900
class AddressForm(forms.ModelForm):
    address_type = forms.ChoiceField(
        choices=AddressType.choices,
        widget=forms.Select(
            attrs={
                # "id": "addresstype",
                "class": "rounded-lg shadow appearance-none w-full border border-gray-300 focus:border-yellow-500 p-2 bg-white focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    street = forms.CharField(
        label=_("Street"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "3 Main St.",
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    city = forms.CharField(
        label=_("City"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("City"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    state = forms.CharField(
        label=_("State"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("State"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    country = forms.CharField(
        label=_("Country"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Country"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    postal_code = forms.CharField(
        label=_("Postal code"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Postal code"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
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
