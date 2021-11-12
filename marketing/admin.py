from django.contrib import admin

from .models import MarketingPreference


class MarketingPreferenceAdmin(admin.ModelAdmin):

    list_display = ("user", "subscribed", "updated")
    readonly_fields = (
        "mailchimp_msg",
        "mailchimp_subscribed",
        "created",
        "updated",
    )

    class Meta:
        model = MarketingPreference
        fields = (
            "user",
            "subscribed",
            "mailchimp_msg",
            "mailchimp_subscribed",
            "created",
            "updated",
        )


admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
