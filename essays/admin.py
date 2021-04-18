from django.contrib import admin

# from django.db import models# from django.utils.html import format_html
from django.forms import ModelForm
# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from .models import Author, Essay

# from tinymce.widgets import TinyMCE


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "bio", "img_tag")
    list_editable = ("bio",)
    prepopulated_fields = {"slug": ("name",)}


# class EssayModelForm(ModelForm):
#     class Meta:
#         model = Essay
#         exclude = ()
#         widgets = {
#             "publish": DjangoToggleSwitchWidget(
#                 round=True, klass="django-toggle-switch-success"
#             ),
#             "recommend": DjangoToggleSwitchWidget(
#                 round=True, klass="django-toggle-dark-primary"
#             ),
#         }


class EssayAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "authors",
        "index",
        "publish",
        "recommend",
        "updated",
        "image_tag",
    )
    # form = EssayModelForm
    list_editable = ("index", "publish", "recommend")
    list_filter = ("updated", "recommend")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    # list_display_links = ['__str__',]

    def authors(self, obj):
        """Combine two fields into one column"""
        if obj.author and obj.author_team:
            return f"{obj.author_team}, {obj.author}"
        else:
            return "Øutis"
        # if obj.author and not obj.author_team:
        #     return f'{obj.author}'
        # else:
        #     return f'{obj.author_team.name}'


class EssaysAdminArea(admin.AdminSite):
    site_header = "Essay Admin"


essays_admin = EssaysAdminArea(name="Essays Admin")

essays_admin.register(Essay, EssayAdmin)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Essay, EssayAdmin)
