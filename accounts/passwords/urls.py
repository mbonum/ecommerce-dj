from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path(
        "change-password/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "change-password/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("reset-password/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset-done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]