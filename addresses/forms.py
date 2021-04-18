"""
/cart/checkout/
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Address


class AddressForm(forms.ModelForm):
    street = forms.CharField(
        label=_("Street"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "3 Main St.",
                "class": "m-auto flex border border-gray-300 focus:outline-none focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2 mb-3 rounded shadow placeholder-gray-900",
            }
        ),
    )
    city = forms.CharField(
        label=_("City"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("City"),
                "class": "m-auto flex border border-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2 mb-3 rounded shadow placeholder-gray-900",
            }
        ),
    )
    state = forms.CharField(
        label=_("State"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("State"),
                "class": "m-auto flex border border-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2 mb-3 rounded shadow placeholder-gray-900",
            }
        ),
    )
    country = forms.CharField(
        label=_("Country"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Country"),
                "class": "m-auto flex border border-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2 mb-3 rounded shadow placeholder-gray-900",
            }
        ),
    )
    postal_code = forms.CharField(
        label=_("Postal/Zip code"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Postal/Zip code"),
                "class": "m-auto flex border border-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2 rounded shadow placeholder-gray-900",
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
        )  # 'billing_profile', 'address_type', 'address_line_1', 'line_2',
