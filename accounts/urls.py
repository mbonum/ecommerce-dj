from django.urls import path

from products.views import UserProductHistoryView

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.AccountHomeView.as_view(), name="user-home"),
    path("details/", views.UserDetailUpdateView.as_view(), name="user-update"),
    path(
        "history/",
        UserProductHistoryView.as_view(),
        name="user-product-history",
    ),
    path(
        "email/confirm/<slug:key>/",
        views.AccountEmailActivateView.as_view(),
        name="email-activate",
    ),
    path(
        "email/resend-activation/",
        views.AccountEmailActivateView.as_view(),
        name="resend-activation",
    ),
]
