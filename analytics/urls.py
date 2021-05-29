from django.urls import path
# from django.utils.translation import gettext_lazy as _
from analytics.views import SalesAjaxView, SalesView

app_name = "analytics"

urlpatterns = [
    path("sales/", SalesView.as_view(), name="sales-analytics"),
    path("sales/data/", SalesAjaxView.as_view(), name="sales-analytics-data"),
]