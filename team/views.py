from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, View
from django.shortcuts import render
from .models import Member


def index(request):
    members = Member.objects.all().order_by("index")  # [:10]
    context = {
        "title": "C-Team",
        "motto": "Qualis Super Quantitas",  # Sumus Clavem E Pluribus Unum
        "team": members,
    }
    return render(request, "team/team.html", context)


def detail(request, slug):
    _m = Member.objects.get(slug=slug)
    context = {
        "member": _m,
    }
    return render(request, "team/team-des.html", context)

# https://www.chartjs.org/docs/latest/charts/radar.html
# class RadarChartAjaxView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         data = {}
#         if request.user.is_admin or request.user.is_staff:
#             qs = Member.objects.all()
#             labels = [
#                 "Finance",
#                 "Technical",
#                 "Design",
#                 "Communication",
#                 "Organization",
#             ]
#             return JsonResponse(data)
#         raise PermissionDenied


# class TeamView(LoginRequiredMixin, TemplateView):
#     template_name = "team/team-des.html"

#     def dispatch(self, *args, **kwargs):
#         user = self.request.user
#         # if user.is_authenticated:
#         if not user.is_staff:  # not user.is_admin
#             raise PermissionDenied
#             # return render(self.request, "400.html", {})  # status=401 403
#         return super(TeamView, self).dispatch(*args, **kwargs)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(TeamView, self).get_context_data(*args, **kwargs)
    #     qs = Member().objects.all()
    #     # context["today"] = today_day
    #     return context
