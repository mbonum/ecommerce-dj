from django.contrib import admin

from .models import Cookie, Donate, Page, Privacy, Terms  # , Section


# class SectionInline(admin.StackedInline):
#     model = Section
#     extra = 2
#     prepopulated_fields = {"slug": ("title",)}


class PrivacyAdmin(admin.ModelAdmin):
    list_display = ("title",)
    # inlines = [SectionInline]
    # form = EssayModelForm
    # list_editable = ("title",)
    # list_filter = ("updated", "recommend")
    # search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


# admin.site.register(Contact)Contact,
admin.site.register(Cookie)
admin.site.register(Donate)
admin.site.register(Page)
admin.site.register(Privacy, PrivacyAdmin)
admin.site.register(Terms)
