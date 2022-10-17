from django.contrib import admin

# from django.db import models# from django.utils.html import format_html
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
# from tinymce.widgets import TinyMCE
from .models import Author, Essay, Section


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


class SectionInline(admin.TabularInline):#StackedInline
    model = Section
    extra = 2
    prepopulated_fields = {"slug": ("title",)}


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
    inlines = [SectionInline]
    # form = EssayModelForm
    list_editable = ("index", "publish", "recommend")
    list_filter = ("updated", "recommend")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    # list_display_links = ['__str__',]

    def authors(self, obj):
        # Combine two fields into one column
        if obj.author and obj.author_team:
            return f"{obj.author_team}, {obj.author}"
        else:
            return "Øutis"
        # if obj.author and not obj.author_team:
        #     return f'{obj.author}'
        # else:
        #     return f'{obj.author_team.name}'


# Add portal for authors
class EssaysAdminArea(admin.AdminSite):
    site_header = _("Essay Admin")


essays_admin = EssaysAdminArea(name=_("Essay Admin"))

essays_admin.register(Essay, EssayAdmin)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Essay, EssayAdmin)
