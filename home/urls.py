from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("trademark/", views.TrademarkView.as_view(), name="trademark"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("donate/", views.DonateView.as_view(), name="donate"),
    path("cookie/", views.CookieView.as_view(), name="cookie"),
    path("privacy/", views.PrivacyView.as_view(), name="privacy"),
    path("terms/", views.TermsView.as_view(), name="terms"),
]
