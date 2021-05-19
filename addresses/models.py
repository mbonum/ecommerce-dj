from billing.models import BillingProfile
from django.db import models
from django.utils.translation import gettext_lazy as _


class AddressType(models.TextChoices):
    BILLING = "B", _("Billing")
    SHIPPING = "S", _("Shipping")

# Check whether the address exists before adding it
class Address(models.Model):
    # User addresses to use for shipping physical products
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=9, choices=AddressType.choices, default=AddressType.BILLING)
    street = models.CharField(max_length=240, default="33 Main St")  # , null=True, blank=True
    # address_line_2 = models.CharField(max_length=90, null=True, blank=True)#apartment, suite or space number
    city = models.CharField(max_length=240)
    state = models.CharField(max_length=240, null=True, blank=True)
    country = models.CharField(max_length=240, default=_("Earth"))
    postal_code = models.CharField(max_length=9)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        address = self.street + "\n" + self.city + "\n"
        if self.state:
            address += self.state + "\n"
        address += self.postal_code + " " + self.country
        return address  #f"{self.street}\n {self.city}\n {self.state}\n {self.postal_code}\n {self.country}"
