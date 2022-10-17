# from urllib.parse import quote_plus
# from datetime import datetime
# # from io import BytesIO
# import requests
# import filecmp
import os
from pathlib import Path

from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from django.utils.translation import gettext as _
from django.views.generic import View
from gtts import gTTS

from core.utils import render_to_pdf
from notes.forms import NoteForm
from notes.models import Note

from .models import Author, Essay

# CreateViewDetailView, ListView, RedirectView
# from django.contrib.auth import get_user
# from django.core.files.storage import default_storage
# from gTTS.cache import remove_cache
# from django.template.loader import get_template, render_to_string
# from django.contrib.auth.models import User
# from rest_framework import authentication, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from analytics.mixins import ObjectViewedMixin
# from django.core.files.base import ContentFile


def essays(request):
    _e = Essay.objects.all().filter(publish=True).order_by("index")
    context = {
        "title": _("Writings"),
        "essays": _e,
    }
    return render(request, "essays/wlist.html", context)


def detail(request, slug: str):
    """
    Show essay
    generate audio
    """
    try:
        essay = Essay.objects.get(slug=slug, publish=True)
    except ObjectDoesNotExist:
        messages.info(
            request,
            _(
                """Sorry, the text is private for now.
                Contact us to know when the product will be published."""
            ),
        )
    p = f"media/essays/{slug}/"
    # str(settings.MEDIA_ROOT) + f"/{slug}/" essay_media_path
    os.makedirs(p, exist_ok=True)
    f = f"{p}{slug}.mp3"  # ogg not supported in mac
    if not essay.audio and not Path(f).is_file():
        # from django.contrib.staticfiles import finders
        # from django.contrib.staticfiles.storage import staticfiles_storage
        # class TestStaticFiles(TestCase):
        # """Check if app contains required static files"""
        # def test_images(self):
        #     abs_path = finders.find('myapp/test.jpg')
        # self.assertTrue(staticfiles_storage.exists(abs_path))
        # https://docs.python.org/3/library/filecmp.html
        # if not filecmp.cmp(Path(f), f, shallow=False):
        e = ""
        for s in essay.section_set.all():
            if s.title:
                e += s.title
            e += s.text
            # payload = f"content={s.text}
            # &response_type=html&request_type=html&fixation=1&saccade=10"
        txt = BeautifulSoup(e, "lxml")  # convert html to text
        tts = gTTS(txt.get_text(), lang="en")
        # if there's a file see if they are the same
        tts.save(f)

    _id = essay.index + 1
    try:
        _next = get_object_or_404(Essay, index=_id)
    except ObjectDoesNotExist:
        _next = None

    # url = "https://bionic-reading1.p.rapidapi.com/convert"

    # headers = {
    #     "content-type": "application/x-www-form-urlencoded",
    #     "X-RapidAPI-Host": "bionic-reading1.p.rapidapi.com",
    #     "X-RapidAPI-Key": "SIGN-UP-FOR-KEY"
    # }

    # response = requests.request("POST", url, data=payload, headers=headers)

    # print(response.text)

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

    all_notes = essay.notes.filter(active=True).order_by("created")

    # Show slider if the notes are more than 3
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
        # "notes": notes, user_note
        "notes": all_notes,
        "pages": notes,
        "next": _next,
    }
    return render(request, "base/txt.html", context)
    # if form.errors:
    #     errors = form.errors.as_json()
    #     if request.accepts("application/json"):
    #         return HttpResponse(errors, status=400, content_type='application/json')


def like_view(request, slug: str, pk: int):
    # Add Bravo (clap) button
    post = get_object_or_404(Note, id=pk)
    post.like.add(request.user)
    return HttpResponseRedirect(reverse("read:detail", args=[str(slug)]))


class GenerateEssayPDF(View):
    # Read Essay's fields in the database and generate pdf
    def get(self, request, **kwargs):  # *args,
        if request.user.email:
            if request.user.first_name:
                n = request.user.first_name
            else:
                e = request.user.email
                # Remove email domain
                n = e[: e.index("@")]
        else:
            n = request.user
        # email = input("what is your email address? ").strip()
        # slice out the domain name
        # domain = email[email.index("@")+1:]
        # email = f"Your username is {user} and your domain name is {domain}""

        slug = kwargs.get("slug")
        # pk = kwargs.get("pk")# edit urls.py and wtxt.html PDF
        essay = Essay.objects.get(slug=slug)
        e = ""
        # s = ""
        for s in essay.section_set.all():
            if s.title:
                e += "<h2>" + s.title + "</h2>"
            e += s.text
        # txt = BeautifulSoup(e, "html.parser") txt.get_text() # "lxml"
        if essay.author is None:
            author = "Øutis"
        else:
            author = essay.author
        author2 = ""
        if essay.author_team and not essay.author:
            author = essay.author_team
        else:
            author2 = essay.author_team
        date = essay.updated.strftime("%Y-%m-%d")
        context = {
            "title": essay.title,
            "author": author,
            "author2": author2,
            "date": date,
            "text": e,
            "n": n,
        }
        pdf = render_to_pdf("essays/pdf/essay.html", context)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = f"{settings.ENV_NAME}_{slug}_{date}.pdf"
            content = f"inline; filename={filename}"
            download = request.GET.get("download")
            if download:
                content = f"attachment; filename={filename}"
            response["Content-Disposition"] = content
            return response
        return HttpResponse(_("Document not found."))


def author_view(request, slug: str):
    # Link to the author's bio
    author = Author.objects.get(slug=slug)
    context = {
        "member": author,
    }
    return render(request, "team/team-des.html", context)
