# /cart/checkout/
import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .models import Address, AddressType


# def validate_zipcode(value):
#     # Check whether the zip code is valid
#     regex_integer_in_range = r"^[1-9]\d{5}$"
#     # isinstance(value, int)
#     regex_alternating_repetitive_digit_pair = r"(\d)(?=\d\1)"
#     five_int = bool(re.match(regex_integer_in_range, value))
#     nr_repetitive_pair = len(re.findall(regex_alternating_repetitive_digit_pair, value))
#     pattern = re.compile(r"\s*(\w\d\s*){3}\s*")
#     try:
#         check_zipcode = pattern.match(value)
#     except check_zipcode is False:
#         messages.info(request, _("Please add a valid postal/zip code"))
# if five_int is False or not nr_repetitive_pair < 2:
#     messages.info(request, _("Please add a valid postal/zip code"))
# return HttpResponse(
#     _("Please add a valid postal/zip code"), status=401
# )
# raise ValidationError(_(f"{value} is an invalid postal/zip code"))


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
        label=_("Street address"),
        widget=forms.TextInput(
            attrs={
                "id": "id_street",
                # "placeholder": "3 Main St. / post office box",
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
        # validators=[validate_zipcode]
    )

    class Meta:
        model = Address
        fields = (
            "street",
            "city",
            "state",
            "country",
            "postal_code",
        )
    # "billing_profile", 'address_type', 'address_line_1', 'line_2',

    # def clean_postalcode(self):
    #     super(AddressForm, self).clean_postalcode()
    #     data = self.cleaned_data["postal_code"]
    #     print("### ", data)
    #     five_int = bool(re.match(regex_integer_in_range, data))
    #     nr_repetitive_pair = len(
    #         re.findall(regex_alternating_repetitive_digit_pair, data)
    #     )
    #     if five_int is False or nr_repetitive_pair < 2:
    #         messages.info(request, _("Please add a valid postal/zip code"))
    #         self._errors["postal_code"] = self.error_class(
    #             ["Please add a valid postal/zip code"]
    #         )
    #         # raise ValidationError(_(f"{data} is an invalid postal/zip code"))
    #     return data

    # def validate(self, value):
    #     """Check if value is a valid zip code."""
    #     # Use the parent's handling of required fields, etc.
    #     super().validate(value)
    #     validate_zipcode(self.postal_code)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["postal_code"].validators.append(validate_zipcode)
