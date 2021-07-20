from django import forms
from django.utils.translation import gettext_lazy as _
from .validators import validate_url


class SubmitURLForm(forms.Form):
    url = forms.CharField(
        label="URL",  # _("Submit URL"),
        widget=forms.TextInput(
            attrs={
                # "placeholder": _("Original URL"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 rounded-xl shadow focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2 py-1 px-2",
            }
        ),
        validators=[validate_url],
    )

    # def clean(self):
    #     url = self.cleaned_data.get("url")#cleaned_data["url"]
    #     if "http" in url:
    #         url = url.replace("http://www.", "")
    #     return url

    #     cleaned_data = super(SubmitURLForm, self).clean()
    #     url = cleaned_data["url"]

    # def clean_url(self):
    #     url = self.cleaned_data["url"]
    #     if "http" in url:
    #         return url
    #     return "http://" + url
    #     url_validator = URLValidator()
    #     try:
    #         url_validator(url)
    #     except:
    #         raise forms.ValidationError(_("Please submit a valid URL"))
    #     return url
