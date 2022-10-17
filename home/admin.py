from django.contrib import admin

from .models import Cookie, Donate, Page, Privacy, Terms, CSection, PSection, TSection


class CSectionInline(admin.TabularInline):  # StackedInline
    model = CSection
    extra = 1
    prepopulated_fields = {"slug": ("title",)}


class CAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [CSectionInline]
    prepopulated_fields = {"slug": ("title",)}


class PSectionInline(admin.TabularInline):
    model = PSection
    extra = 1
    prepopulated_fields = {"slug": ("title",)}


class PAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [PSectionInline]
    prepopulated_fields = {"slug": ("title",)}
    # form = EssayModelForm
    # list_editable = ("title",)
    # list_filter = ("updated",)
    # search_fields = ("title",)


class TSectionInline(admin.TabularInline):
    model = TSection
    extra = 1
    prepopulated_fields = {"slug": ("title",)}


class TAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [TSectionInline]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Cookie, CAdmin)
admin.site.register(Donate)
admin.site.register(Page)
admin.site.register(Privacy, PAdmin)
admin.site.register(Terms, TAdmin)
