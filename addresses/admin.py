from django.contrib import admin

from .models import Address


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ("billing_profile", "address_type", "street", "city", "state", "country", "postal_code", "created_at", "updated_at")
    list_filter = ("country",)
    search_fields = ("country",)


admin.site.register(Address, AddressAdmin)
