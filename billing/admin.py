from django.contrib import admin

from .models import BillingProfile, Card, Charge


class BillingProfileAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "email", "customer_id", "active")
    list_filter = ("active",)  # list_display


class CardAdmin(admin.ModelAdmin):
    readonly_fields = (
        "billing_profile",
        "stripe_id",
        "brand",
        "country",
        "exp_month",
        "exp_year",
        "last4",
        "default",
        "active",
        "created_at",
    )
    list_filter = ("active",)


class ChargeAdmin(admin.ModelAdmin):
    readonly_fields = (
        "billing_profile",
        "stripe_id",
        "paid",
        "refunded",
        "outcome",
        "outcome_type",
        "seller_message",
        "risk_level",
    )
    list_filter = ("risk_level",)


admin.site.register(BillingProfile, BillingProfileAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Charge, ChargeAdmin)
