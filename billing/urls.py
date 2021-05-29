from django.urls import path

# from django.utils.translation import gettext_lazy as _
from billing.views import payment_method_createview, payment_method_view

app_name = "billing"

urlpatterns = [
    path("payment-method/", payment_method_view, name="billing-payment-method"),
    path(
        "payment-method/create/",
        payment_method_createview,
        name="billing-payment-method-end",
    ),
]