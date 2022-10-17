from django.contrib import admin

from .models import ClickEvent, ObjectViewed, UserSession


class ClickEventAdmin(admin.ModelAdmin):
    readonly_fields = ('count',)


class ObjectViewedAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "ip_address", "content_type", "object_id", "content_object", "created")
    list_filter = ("created",)


class UserSessionAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "session_key", "ip_address", "created")
    list_filter = ("active",)


admin.site.register(ClickEvent, ClickEventAdmin)
admin.site.register(ObjectViewed, ObjectViewedAdmin)
admin.site.register(UserSession, UserSessionAdmin)
