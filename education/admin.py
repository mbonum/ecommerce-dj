from django.contrib import admin
from django.forms import ModelForm
# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from .models import Book


# class BookModelForm(ModelForm):
#     class Meta:
#         model = Book
#         exclude = ()
#         widgets = {
#             "active": DjangoToggleSwitchWidget(
#                 round=True, klass="django-toggle-switch-success"
#             ),
#         }


class BookAdmin(admin.ModelAdmin):
    # form = BookModelForm
    list_display = ("title", "index", "created", "img_tag")
    list_editable = ("index",)
    list_filter = ("created",)
    prepopulated_fields = {"slug": ("title",)}

    class Meta:
        model = Book


admin.site.register(Book, BookAdmin)
