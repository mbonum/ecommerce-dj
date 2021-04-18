from django.contrib import admin

from .models import ClickEvent, ObjectViewed, UserSession


class ClickEventAdmin(admin.ModelAdmin):
    readonly_fields = ('count',)


class ObjectViewedAdmin(admin.ModelAdmin):
    list_display = ("user", "content_object", "ip_address", "created_at")
    list_filter = ("created_at",)


class UserSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "created_at")
    list_filter = ("active",)


admin.site.register(ClickEvent, ClickEventAdmin)
admin.site.register(ObjectViewed, ObjectViewedAdmin)
admin.site.register(UserSession, UserSessionAdmin)
