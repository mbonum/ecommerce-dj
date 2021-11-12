from django import forms
# from django.contrib.auth import get_user_model# from django.db.models import fields 'cols':30,
# from tinymce.widgets import TinyMCE#https://django-tinymce.readthedocs.io/en/latest/usage.html?highlight=attrs
from mptt.forms import TreeNodeChoiceField

from .models import Review


class ReviewForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Review.objects.all())  # level_indicator='>--'
    body = forms.CharField(
        label="",
        required=True,
        widget=forms.Textarea(
            attrs={
                "id": "id_rev",
                "rows": 4,
                # "placeholder": "Clear, concise, ideally, compelling",#"class": "w-full text-black tracking-wide border border-gray-400 hover:border-yellow-500 focus:border-yellow-500 rounded-lg py-2 px-3 placeholder-gray-800 shadow hover:shadow-md focus:outline-none focus:ring-2 ring-yellow-200 ring-offset-transparent ring-offset-2 py-1 px-2 mt-2",#"autocapitalize": "sentences",
                "spellcheck": "true",
                "type": "text",
                "class": "w-full hover:border-yellow-500 focus:border-yellow-500 cr2"
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].widget.attrs.update({"class": "hidden"})
        self.fields["parent"].label = ""
        self.fields["parent"].required = False

    class Meta:
        model = Review
        fields = (
            "parent",
            "body",
            # "private",
        )

    def save(self, *args, **kwargs):
        Review.objects.rebuild()
        return super(ReviewForm, self).save(*args, **kwargs)
