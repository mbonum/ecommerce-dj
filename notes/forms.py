from django import forms

# from django.contrib.auth import get_user_model
# from django.db.models import fields 'cols':30,
# from tinymce.widgets import TinyMCE https://django-tinymce.readthedocs.io/en/latest/usage.html?highlight=attrs
from mptt.forms import TreeNodeChoiceField

from .models import Note


class NoteForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Note.objects.all())
    body = forms.CharField(
        label="",
        required=True,
        widget=forms.Textarea(
            attrs={
                "id": "comment",
                "rows": 4,
                "placeholder": "Clear, concise, ideally, compelling",
                "class": "hover:border-yellow-600 w-full tracking-wide border border-gray-500 rounded-lg text-black py-2 px-3 placeholder-gray-800 hover:shadow-md focus:ring-2 ring-yellow-200 ring-offset-transparent ring-offset-2 py-1 px-2 mt-2",
                "type": "text",
            }
        ),
    )
    private = forms.BooleanField(
        label="",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "name": "anonym",
                "class": "transform hover:scale-110",
                # "data-tippy-content": "Anonym",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].widget.attrs.update({"class": "hidden"})
        self.fields["parent"].label = ""
        self.fields["parent"].required = False

    class Meta:
        model = Note
        fields = (
            "parent",
            "body",
            "private",
        )


# js = ('/static/js/tinymce.js',)Everyone knows something someone else doesn't.
# <script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js" referrerpolicy="origin"></script>
