# from urllib.parse import quote_plus
# from datetime import datetime
# from django.contrib.auth import get_user
import filecmp
import os
from pathlib import Path

from bs4 import BeautifulSoup
from core.utils import render_to_pdf
from django.conf import settings

# from django.contrib.contenttypes.models import ContentType

# from io import BytesIO
# from django.core.files.storage import default_storage
# from gTTS.cache import remove_cache
# from django.template.loader import get_template, render_to_string
# from django.contrib.auth.models import User
# from rest_framework import authentication, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from analytics.mixins import ObjectViewedMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect  # JsonResponse Http404
from django.shortcuts import get_object_or_404, render  # redirect

# from django.core.files.base import ContentFile
from django.urls.base import reverse  # reverse_lazy
from django.utils.translation import gettext as _

# CreateViewDetailView, ListView, RedirectView
from django.views.generic import View
from gtts import gTTS
from notes.forms import NoteForm
from notes.models import Note

from .models import Author, Essay  # , Section


def index(request):
    essays = Essay.objects.all().filter(publish=True).order_by("index")
    context = {
        "title": _("Writings"),
        "essays": essays,
    }
    return render(request, "essays/wlist.html", context)


def details(request, slug: str):
    """
    Show essay
    generate audio
    """
    essay = get_object_or_404(Essay, slug=slug, publish=True)
    path = "static/media_root/essays/" + f"{slug}/"
    # # access on cdn getattr(settings, "MEDIA_ROOT") + "/essays/"
    os.makedirs(path, exist_ok=True)
    f = f"{path}{slug}.mp3"  # static/media_root ogg not supported in mac
    if not essay.audio and not Path(f).is_file():
        # if not filecmp.cmp(Path(f), f, shallow=False):
        e = ""
        for s in essay.section_set.all():
            if s.title:
                e += s.title
            e += s.text
        txt = BeautifulSoup(e, "lxml")  # convert html to text
        tts = gTTS(txt.get_text(), lang="en")
        # 'static' + settings.MEDIA_URL + 'essays/' + f'{slug}/'#/media_root/
        # if there's a file see if they are the same
        # https://docs.python.org/3/library/filecmp.html
        tts.save(f)

    _id = essay.index + 1
    try:
        _next = get_object_or_404(Essay, index=_id)
    except:
        _next = None

    user_note = None
    if request.method == "POST":
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            user_note = note_form.save(commit=False)
            user_note.essay = essay
            user_note.user = request.user
            user_note.save()
            return HttpResponseRedirect(essay.get_absolute_url())
    else:
        note_form = NoteForm()

    all_notes = essay.notes.filter(active=True).order_by("created_at")
    paginator = Paginator(all_notes, 3)
    page = request.GET.get("page", 1)
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    context = {
        "object": essay,
        "tts": f,
        "form": note_form,
        # "notes": notes,user_note
        "notes": all_notes,
        "pages": notes,
        "next": _next,
    }
    return render(request, "essays/wtext.html", context)
    # if form.errors:
    #     errors = form.errors.as_json()
    #     if request.is_ajax():
    #         return HttpResponse(errors, status=400, content_type='application/json')


def like_view(request, slug: str, pk: int):
    # Add like
    post = get_object_or_404(Note, id=pk)  # request.POST.get['post_id']
    post.like.add(request.user)
    return HttpResponseRedirect(reverse("read:detail", args=[str(slug)]))


class GenerateEssayPDF(View):
    def get(self, request, *args, **kwargs):
        if request.user.email:
            if request.user.first_name:
                n = request.user.first_name
            else:
                e = request.user.email
                n = e[: e.index("@")]  # slice out username
        else:
            n = request.user
        # email = input("what is your email address? ").strip()
        # slice out the domain name
        # domain = email[email.index("@")+1:]
        # email = f'Your username is {user} and your domain name is {domain}'

        # s = kwargs.get("slug")
        # essay = Essay.objects.get(slug=s)
        # Use essay's pk (id) to link with the foreign key in Section
        pk = kwargs.get("pk")
        essay = Essay.objects.get(id=pk)
        e = ""
        # s = ""
        for s in essay.section_set.all():
            if s.title:
                e += s.title
            e += s.text
        txt = BeautifulSoup(e, "lxml")
        if essay.author is None:
            author = "Øutis"
        else:
            author = essay.author
        author2 = ""
        if essay.author_team and not essay.author:
            author = essay.author_team
        else:
            author2 = essay.author_team
        context = {
            "title": essay.title,
            "author": author,
            "author2": author2,
            "date": essay.updated,
            "text": txt,
            "n": n,
        }
        pdf = render_to_pdf("essays/pdf/essay.html", context)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = f"{settings.BASE_URL}_{s}.pdf"
            content = f"inline; filename={filename}"
            download = request.GET.get("download")
            if download:
                content = f"attachment; filename={filename}"
            response["Content-Disposition"] = content
            return response
        return HttpResponse(_("Document not found."))


def author_view(request, slug: str):
    # Open independent author's bio page
    author = Author.objects.get(slug=slug)
    context = {
        "member": author,
    }
    return render(request, "team/team-des.html", context)
