from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse  # , HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View

from orders.models import Order


class SalesAjaxView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_staff:
            qs = Order.objects.all().by_weeks_range(weeks_ago=5, number_of_weeks=5)
            if request.GET.get("type") == "week":
                days = 7  # today included
                start_date = timezone.now().today() - timezone.timedelta(days=days - 1)
                datetime_list = []
                labels = []
                sales_items = []
                for current in range(0, days):
                    new_time = start_date + timezone.timedelta(days=current)
                    datetime_list.append(new_time)
                    labels.append(new_time.strftime("%a"))  # format weekdays e.g. Mon
                    new_qs = qs.filter(updated__day=new_time.day, updated__month=new_time.month)
                    day_total = new_qs.totals_data()["total__sum"] or 0
                    sales_items.append(day_total)
                data["labels"] = labels
                data["data"] = sales_items
            if request.GET.get("type") == "4weeks":
                data["labels"] = [
                    _("Four weeks ago"),
                    _("Three weeks ago"),
                    _("Two weeks ago"),
                    _("Last week"),
                    _("This week"),
                ]
                current = 5
                data["data"] = []
                for _ in range(0, 5):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
                    sales_total = new_qs.totals_data()["total__sum"] or 0
                    data["data"].append(sales_total)
                    current -= 1
        return JsonResponse(data)


class SalesView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/sales.html"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return render(self.request, "400.html", {})  # status=401
        return super(SalesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args, **kwargs)
        qs = Order.objects.all().by_weeks_range(weeks_ago=10, number_of_weeks=10)
        start_date = timezone.now().date() - timezone.timedelta(hours=24)
        end_date = timezone.now().date() - timezone.timedelta(hours=12)
        today_day = qs.by_range(start_date=start_date, end_date=end_date).get_sales_breakdown()
        context["today"] = today_day
        context["this_week"] = qs.by_weeks_range(weeks_ago=1, number_of_weeks=1).get_sales_breakdown()
        context["last_four_weeks"] = qs.by_weeks_range(weeks_ago=5, number_of_weeks=4).get_sales_breakdown()
        return context
