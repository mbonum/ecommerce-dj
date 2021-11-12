from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("trademark/", views.TrademarkView.as_view(), name="trademark"),
    path("donate/", views.DonateView.as_view(), name="donate"),
    path("cookie/", views.CookieView.as_view(), name="cookie"),
    path("privacy/", views.PrivacyView.as_view(), name="privacy"),
    path("terms/", views.TermsView.as_view(), name="terms"),
    path("policy-pdf/<slug:slug>/", views.GeneratePolicyPDF.as_view(), name="policy-pdf"),
]
