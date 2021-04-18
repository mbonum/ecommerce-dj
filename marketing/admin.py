from django.contrib import admin

from .models import MarketingPreference


class MarketingPreferenceAdmin(admin.ModelAdmin):

    list_display = ("user", "subscribed", "updated_at")
    readonly_fields = (
        "mailchimp_msg",
        "mailchimp_subscribed",
        "timestamp",
        "updated_at",
    )

    class Meta:
        model = MarketingPreference
        fields = (
            "user",
            "subscribed",
            "mailchimp_msg",
            "mailchimp_subscribed",
            "timestamp",
            "updated_at",
        )


admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
