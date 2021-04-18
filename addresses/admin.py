from django.contrib import admin

from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ("billing_profile", "country")
    list_filter = ("country",)
    # search_fields = ()


admin.site.register(Address, AddressAdmin)
