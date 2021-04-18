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


def details(request, slug):
    _m = Member.objects.get(slug=slug)
    context = {
        "member": _m,
    }
    return render(request, "team/team-des.html", context)
