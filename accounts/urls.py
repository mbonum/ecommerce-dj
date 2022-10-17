from django.urls import path
from django.utils.translation import gettext_lazy as _

from shop.views import UserProductHistoryView

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.AccountHomeView.as_view(), name="user-home"),
    path(_("profile/"), views.UserDetailUpdateView.as_view(), name="user-update"),
    path(
        _("history/"),
        UserProductHistoryView.as_view(),
        name="user-product-history",
    ),
    path(
        _("email/confirm/<slug:key>/"),
        views.AccountEmailActivateView.as_view(),
        name="email-activate",
    ),
    path(
        _("email/resend-activation/"),
        views.AccountEmailActivateView.as_view(),
        name="resend-activation",
    ),
]
