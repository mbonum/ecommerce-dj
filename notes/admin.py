from django.contrib import admin

# from django.forms import ModelForm
# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from mptt.admin import MPTTModelAdmin
from .models import Note


# class NoteModelForm(ModelForm):
#     class Meta:
#         model = Note
#         exclude = []
#         widgets = {
#             'private': DjangoToggleSwitchWidget(round=True, klass='django-toggle-switch-success'),
#             'reply': DjangoToggleSwitchWidget(round=True, klass='django-toggle-switch-success'),
#             'show': DjangoToggleSwitchWidget(round=True, klass='django-toggle-dark-primary')
#         }

# @admin.register(models.Essay)
# class NoteAdmin(admin.ModelAdmin):
#     list_display = ['user', 'body', 'created',]
#     form = NoteModelForm
#     list_filter = ['created']

admin.site.register(Note, MPTTModelAdmin)
