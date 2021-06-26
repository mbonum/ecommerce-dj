import filecmp
import os
from pathlib import Path

from django.conf import settings

# from core.utils import render_to_pdf
from bs4 import BeautifulSoup  # pip install beautifulsoup4

# from django.http import HttpResponse# Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView  # DetailView, View
from gtts import gTTS  # pip install gTTS

from .models import Book  # , book_media_path


class ReadListView(ListView):
    template_name = "education/blist.html"

    def get_queryset(self, *args, **kwargs):
        return Book.objects.all().filter(active=True).order_by("index")


def details(request, slug):
    book = get_object_or_404(Book, slug=slug)
    p = "media/edu/{slug}/"
    # str(settings.MEDIA_ROOT) + f"{slug}" str(settings.MEDIA_ROOT + book_media_path(f"{slug}", f"{slug}") + ".mp3")
    os.makedirs(p, exist_ok=True)
    f = f"{p}{slug}.mp3"
    if not book.audio and not Path(f).is_file():
        b = ""
        for s in book.section_set.all():
            if s.title:
                b += s.title
            b += s.text
        txt = BeautifulSoup(b, features="lxml")
        tts = gTTS(txt.get_text(), lang="en")
        # if Path(f).is_file() and not filecmp.cmp(Path(f), f"{p}{slug}.mp3", shallow=True):
        #         tts.save(f)
        tts.save(f)

    _id = book.index + 1
    try:
        _next = get_object_or_404(Book, index=_id)
    except:
        _next = None
    context = {"object": book, "tts": f, "next": _next}
    return render(request, "base/text.html", context)


# class ReadDetailSlugView(DetailView):

#     queryset = Book.objects.all()
#     template_name = 'education/bnotes.html'

#     def get_object(self, *args, **kwargs):
#         # request = self.request
#         slug = self.kwargs.get('slug')
#         instance = get_object_or_404(Book, slug=slug, active=True)
#         # try:
#         #     instance = Book.objects.get(slug=slug, active=True)
#         # except Book.DoesNotExist:
#         #     raise Http404('Not found, sorry')
#         # except Book.MultipleObjectsReturned:
#         #     qs = Book.objects.filter(slug=slug, active=True)
#         # if instance.MultipleObjectsReturned:
#         #     instance = instance.first()
#         # except:
#         #     raise Http404("We're puzzled?!")
#         return instance

# def index(request):
#     """Show the list of essays"""
#     b = Book.objects.all().filter(active=True).order_by('index')

#     context = {
#         # 'title': 'Ideas to be aware of',
#         'object_list': b,
#     }
#     return render(request, 'education/blist.html', context)

# class GenerateEduPDF(View):
#     def get(self, request, *args, **kwargs):
#         s = kwargs.get('slug')
#         b = Book.objects.get(slug=s)
#         txt = b.text
#         # sec2 = essay.sec2
#         # sec3 = essay.sec3
#         author = b.author
#         author2 = None
#         # if b.author_team and not b.author:
#         #     author = esbsay.author_team
#         # else:
#         #     author2 = b.author_team
#         context = {
#             'title': b.title,
#             # 'author': author,
#             'date': b.updated,
#             'text': txt,
#         }
#         # html = template.render(context)
#         # pypandoc.convert_file(html)
#         pdf = render_to_pdf('edu/pdf/book.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = f'{BASE_URL}_{s}.pdf'
#             content = f'inline; filename={filename}'
#             download = request.GET.get('download')
#             if download:
#                 content = f'attachment; filename={filename}'
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse('Document not found.')
