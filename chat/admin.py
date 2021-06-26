from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    # form =
    list_display = (
        "username",
        "room",
        "text",
        "sent",
    )
    list_filter = ("sent",)


admin.site.register(Message, MessageAdmin)
