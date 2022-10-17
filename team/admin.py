from django.contrib import admin
from django.forms import ModelForm

# from django.db import models
# from pagedown.widgets import AdminPagedownWidget#, PagedownWidget
from .models import Member


# class TeamModelForm(ModelForm):
#     class Meta:
#         model = Member
#         exclude = []
#         widgets = {
#             # "published": DjangoToggleSwitchWidget(klass="django-toggle-switch-dark-primary"),
#             "show": DjangoToggleSwitchWidget(
#                 round=True, klass="django-toggle-switch-success"
#             ),
#         }


class TeamAdmin(admin.ModelAdmin):

    # formfield_overrides = {
    #     models.TextField: {'widget': AdminPagedownWidget},
    # }
    # form = TeamModelForm
    list_display = (
        "name",
        "index",
        "job_title",
        "bio",
        "img_tag",
    )  # 'active' 'combine_name_img',
    # list_display_links = ('__str__',)
    list_editable = (
        "index",
        "job_title",
        "bio",
    )
    list_filter = ("job_title",)
    search_fields = (
        "name",
        "job_title",
    )
    prepopulated_fields = {"slug": ("name",)}

    # def combine_name_img(self, obj):
    #     """Combine two fields into one column of the CMS table"""
    #     if obj.image_tag:
    #         return f'{obj.name} - {obj.image_tag}'
    #     else:
    #         return f'{obj.name}'


admin.site.register(Member, TeamAdmin)
