from django.urls import path
from django.utils.translation import gettext_lazy as _
from addresses.views import (
    AddressCreateView,
    AddressListView,
    AddressUpdateView,
    checkout_address_create_view,
    checkout_address_reuse_view,
)

app_name = "addresses"

urlpatterns = [
    path("", AddressListView.as_view(), name="addresses"),
    path(_("create/"), AddressCreateView.as_view(), name="address-create"),
    path(_("<int:pk>/"), AddressUpdateView.as_view(), name="address-update"),
    path(
        _("checkout/address/create/"),
        checkout_address_create_view,
        name="checkout_address_create",
    ),
    path(
        _("checkout/address/reuse/"),
        checkout_address_reuse_view,
        name="checkout_address_reuse",
    ),
]
