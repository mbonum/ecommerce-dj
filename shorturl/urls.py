from django.urls import path, re_path
from . import views

app_name = "shorturl"

urlpatterns = [
    path("", views.ShortURLView.as_view(), name="curl"),
    # only for admin
    re_path(r"^(?P<shortcode>[\w-]+)/$", views.URLRedirectView.as_view(), name="code"),
    # models.get_short_url
]