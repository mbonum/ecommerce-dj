# from urllib.parse import quote_plus
# from datetime import datetime
# from django.contrib.auth import get_user
import filecmp
import os
from pathlib import Path

from django.conf import settings
from core.utils import render_to_pdf
from bs4 import BeautifulSoup

# from django.contrib.contenttypes.models import ContentType
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from io import BytesIO
# from django.core.files.storage import default_storage
# from gTTS.cache import remove_cache
# from django.template.loader import get_template, render_to_string
# from django.contrib.auth.models import User
# from rest_framework import authentication, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from analytics.mixins import ObjectViewedMixin
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

from .models import Author, Essay


def index(request):
    essays = Essay.objects.all().filter(publish=True).order_by("index")
    context = {
        "title": _("Writings"),
        "essays": essays,
    }
    return render(request, "essays/wlist.html", context)


# def stripTags(html, invalid_tags):
#     soup = BeautifulSoup(html, "lxml")

#     for tag in soup.findAll(True):
#         if tag.name in invalid_tags:
#             s = "::"
#             for c in tag.contents:
#                 if not isinstance(c, NavigableString):
#                     c = stripTags(str(c), invalid_tags)
#                 s += str(c)
#             tag.replaceWith(s)
#     return soup


def details(request, slug: str):
    """
    Show essay
    generate audio
    """
    essay = get_object_or_404(Essay, slug=slug, publish=True)
    if not essay.audio:
        path = getattr(settings, "MEDIA_ROOT") + "/essays/" + f"{slug}/"
        os.makedirs(path, exist_ok=True)
        f = f"{path}{slug}.mp3"  # static/media_root ogg not supported in mac
        e = ""
        for s in essay.section_set.all():
            if s.title:
                e += s.title
            e += s.text
        # invalid_tags = ["br", "b", "font"]
        # txt = stripTags(e, invalid_tags)
        txt = BeautifulSoup(e, "lxml")  # features= convert html to text
        tts = gTTS(txt.get_text(), lang="en")
        # 'static' + settings.MEDIA_URL + 'essays/' + f'{slug}/'#/media_root/
        if Path(f).is_file():  # if there's a file see if they are the same
            # https://docs.python.org/3/library/filecmp.html
            if not filecmp.cmp(Path(f), f, shallow=False):
                tts.save(f)
        else:
            tts.save(f)

    _id = essay.index + 1
    try:
        _next = get_object_or_404(Essay, index=_id)
    except:
        _next = None

    cmts = Note.objects.filter(active=True)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(all_cmts, 3)
    # try:
    #     cmts = paginator.page(page)
    # except PageNotAnInteger:
    #     cmts = paginator.page(1)
    # except EmptyPage:
    #     cmts = paginator.page(paginator.num_pages)

    form = NoteForm(request.POST or None)
    if form.is_valid():  # request.method == 'POST'
        parent = form.cleaned_data.get("parent")
        b = form.cleaned_data.get("body")  # or request.POST.get('body')
        p = form.cleaned_data.get("private")  # or request.POST.get('private')
        p = False if p is None or p == "on" else True  # privacy by default
        new_note, created = Note.objects.get_or_create(
            user=request.user,
            essay=essay,
            parent=parent,
            body=b,
            private=p,
        )
        return HttpResponseRedirect("")
    # print('**', f)
    context = {"essay": essay, "tts": f, "form": form, "notes": cmts, "next": _next}
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
        # essay_id = kwargs.get('id')
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
        s = kwargs.get("slug")
        essay = Essay.objects.get(slug=s)
        text = essay.text
        if essay.author is None:
            author = "Øutis"
        else:
            author = essay.author
        author2 = None
        if essay.author_team and not essay.author:
            author = essay.author_team
        else:
            author2 = essay.author_team
        context = {
            "title": essay.title,
            "author": author,
            "author2": author2,
            "date": essay.updated,
            "text": text,
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
        return HttpResponse("Document not found.")


def author_view(request, slug: str):
    # Open independent author's bio page
    author = Author.objects.get(slug=slug)
    context = {
        "member": author,
    }
    return render(request, "team/team-des.html", context)
