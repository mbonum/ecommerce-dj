from django.contrib import admin

from .models import BillingProfile, Card, Charge


class BillingProfileAdmin(admin.ModelAdmin):

    readonly_fields = ("user", "customer_id", "active")
    list_filter = ("active",)  # list_display


admin.site.register(BillingProfile, BillingProfileAdmin)
admin.site.register(Card)
admin.site.register(Charge)
