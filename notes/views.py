from django.shortcuts import render  # , get_object_or_404, HttpResponseRedirect
from .models import Note
from .forms import NoteSearchForm

# from django.views.generic import ListView
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def post_search(request):
    form = NoteSearchForm
    q = ""
    c = ""
    results = []
    query = Q()

    if "q" in request.GET:
        form = NoteSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data["q"]
            c = form.cleaned_data["c"]

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Note.objects.filter(query)

    return render(request, "search.html", {"form": form, "q": q, "results": results})
