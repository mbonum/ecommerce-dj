import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse  # , HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from orders.models import Order
from accounts.models import CURRENCIES  # , CurrencyType

# from forex_python.converter import CurrencyRates
# from currency_converter import CurrencyConverter

# def exchange_rate():
#     c = CurrencyRates()
#     c.get_rate('EUR', 'USD')


class SalesAjaxView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_admin or request.user.is_staff:
            qs = Order.objects.all().by_weeks_range(weeks_ago=5, number_of_weeks=5)
            if request.GET.get("type") == "week":
                days = 7  # today included
                start_date = timezone.now().today() - datetime.timedelta(days=days - 1)
                datetime_list = []
                labels = []
                sales_items = []
                for d in range(0, days):
                    new_time = start_date + datetime.timedelta(days=d)
                    datetime_list.append(new_time)
                    labels.append(new_time.strftime("%a"))  # format weekdays e.g. Mon
                    new_qs = qs.filter(
                        updated__day=new_time.day, updated__month=new_time.month
                    )
                    day_total = new_qs.totals_data()["total__sum"] or 0
                    sales_items.append(day_total)
                data["labels"] = labels
                data["data"] = sales_items
            if request.GET.get("type") == "4weeks":
                data["labels"] = [
                    "Four weeks ago",
                    "Three weeks ago",
                    "Two weeks ago",
                    "Last week",
                    "This week",
                ]
                current = 5
                data["data"] = []
                for _ in range(0, 5):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
                    sales_total = new_qs.totals_data()["total__sum"] or 0
                    data["data"].append(sales_total)
                    current -= 1
            return JsonResponse(data)
        raise PermissionDenied


class SalesView(LoginRequiredMixin, TemplateView):  # View
    template_name = "analytics/sales.html"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        # if user.is_authenticated:
        if not user.is_staff:  # not user.is_admin or
            raise PermissionDenied
            # return render(self.request, "400.html", {})  # status=401 403
        return super(SalesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args, **kwargs)
        qs = Order.objects.all().by_weeks_range(weeks_ago=10, number_of_weeks=10)
        start_date = timezone.now().date() - timezone.timedelta(hours=24)
        end_date = timezone.now().date() - timezone.timedelta(hours=12)
        today_day = qs.by_range(
            start_date=start_date, end_date=end_date
        ).get_sales_breakdown()
        context["today"] = today_day
        context["this_week"] = qs.by_weeks_range(
            weeks_ago=1, number_of_weeks=1
        ).get_sales_breakdown()
        context["last_four_weeks"] = qs.by_weeks_range(
            weeks_ago=5, number_of_weeks=4
        ).get_sales_breakdown()
        context["currencies"] = CURRENCIES
        # print(CURRENCIES[1])  # CurrencyType.EUR)
        return context


# pip install currencyconverter
# co = CurrencyConverter()
# print(co.convert(1, "EUR", "USD"))

# forex-python
# c = CurrencyRates()
# eur_usd = float(c.get_rate("EUR", "USD"))
# force_decimal=True c.get_symbol('EUR')
# context["eur_usd"] = eur_usd  # round(eur_usd, 2)
# format(eur_usd, ".2f")
# float("%.2f" % (eur_usd))
