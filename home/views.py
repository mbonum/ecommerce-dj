# import os
# from mimetypes import guess_type
# from wsgiref.util import FileWrapper
# from core.utils import unique_slug_generator
# from django.conf import settings

from io import BytesIO

# from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage, send_mail
from django.http import FileResponse, HttpResponse  # , JsonResponse#Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView  # FormView
from django.views.generic.edit import FormView  # get_language, activate
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .forms import ContactForm
from .models import Cookie, Donate, Page, Privacy, Terms, Trademark

# from core.utils import render_to_pdf
# from subscribe.forms import JoinForm


def policy_pdf(request):
    buffer = BytesIO()

    p = canvas.Canvas(buffer)

    p.drawString(100, 100, "Hello world.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename="hello.pdf"
    )  #  # download pop up

    # fileName = "sample.pdf"
    # documentTitle = "sample"
    # title = "Technology"
    # subTitle = "The largest thing now!!"
    # textLines = [
    #     "Technology makes us aware of",
    #     "the world around us.",
    # ]
    # image = "image.jpg"

    # pdf = canvas.Canvas(fileName)
    # pdf.setTitle(documentTitle)
    # pdfmetrics.registerFont(TTFont("clvm", "PT-Root-UI_Regular.ttf"))

    # pdf.setFont("clvm", 36)
    # pdf.drawCentredString(300, 770, title)

    # pdf.setFillColorRGB(0, 0, 255)
    # pdf.setFont("Courier-Bold", 24)
    # pdf.drawCentredString(290, 720, subTitle)

    # # drawing a line
    # pdf.line(30, 710, 550, 710)

    # # creating a multiline text using
    # # textline and for loop
    # text = pdf.beginText(40, 680)
    # text.setFont("Courier", 18)
    # text.setFillColor(colors.red)

    # for line in textLines:
    #     text.textLine(line)

    # pdf.drawText(text)

    # pdf.drawInlineImage(image, 130, 400)

    # # saving the pdf
    # pdf.save()

    # response = HttpResponse(content_type="application/pdf")
    # d = datetime.today().strftime("%Y-%m-%d")
    # response["Content-Disposition"] = f"inline; filename={d}.pdf"
    # buffer = BytesIO()
    # p = canvas.Canvas(buffer, pagesize=A4)
    # data = {}
    # p.setFont("", 12, leading=None)
    # p.setFillColorRGB()
    # p.drawString(260,800, "Clavem")
    # p.line()
    # x1 =
    # y1 =
    # p.setTitle(f"Policy {d}")
    # p.showPage()
    # p.save()))
    # pdf.buffer.getvalue()
    # buffer.close()
    # response.write(pdf)
    # return response


class HomeView(SuccessMessageMixin, CreateView):
    template_name = "home/home.html"
    model = Page
    fields = "__all__"
    success_url = "/"

    def get_queryset(self):
        return Page.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["page_obj"] = HomeView.get_queryset(self)
        return context


# def home(request):
#     # Multilingual
#     trans = translate(lang='de')
#     return(request, 'home.html', {'trans': trans})

# def translate(lang):
#     cur_lang = get_language()
#     try:
#         activate(lang)
#     finally:
#         activate(cur_lang)


class DonateView(CreateView):
    template_name = "home/donate.html"
    success_url = "/donate/"
    model = Donate
    fields = "__all__"

    def get_queryset(self):
        return Donate.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(DonateView, self).get_context_data(*args, **kwargs)
        context["text"] = DonateView.get_queryset(self)
        return context


class CookieView(CreateView):
    template_name = "base/text.html"  # home/policy.html"  #'policies/cookie.html'
    success_url = "/cookie/"
    model = Cookie
    fields = "__all__"

    def get_queryset(self):
        return Cookie.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(CookieView, self).get_context_data(*args, **kwargs)
        context["object"] = CookieView.get_queryset(self)
        # context['download'] = CookieView.get_download_url(self)
        return context

    # def get_download_url(self):
    #     fileroot = settings.MEDIA_ROOT
    #     filepath = self  # .url /media/cookie
    #     final_filepath = os.path.join(
    #         fileroot, filepath)  # where the file is stored
    #     with open(final_filepath, 'rb') as _f:
    #         wrapper = FileWrapper(_f)
    #         # content = 'some'
    #         mimetype = 'application/force-download'  # 'text/plain' for a txt file
    #         # look the extension of the first [0] file
    #         guessed_mimetype = guess_type(filepath)[0]
    #         if guessed_mimetype:
    #             mimetype = guessed_mimetype
    #         response = HttpResponse(wrapper, content_type=mimetype)  # content
    #         response["Content-Disposition"] = f'attachment;filename={self.pdf_name}'
    #         response["X-SendFile"] = str(self.pdf_name)
    #         return response


# def download(request, path):
# file_path = os.path.join(settings.MEDIA_ROOT, path)
# if os.path.exists(file_path):
#     with open(file_path, 'rb') as fh:
#         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#         return response
# raise Http404


class PrivacyView(CreateView):
    template_name = "base/text.html"  #'policies/privacy.html'
    success_url = "/privacy/"
    model = Privacy
    fields = "__all__"

    def get_queryset(self):
        return Privacy.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(PrivacyView, self).get_context_data(*args, **kwargs)
        context["object"] = PrivacyView.get_queryset(self)
        return context


class TermsView(CreateView):
    template_name = "base/text.html"
    success_url = "/terms/"
    model = Terms
    fields = "__all__"

    def get_queryset(self):
        return Terms.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(TermsView, self).get_context_data(*args, **kwargs)
        context["object"] = TermsView.get_queryset(self)
        return context


class TrademarkView(CreateView):
    template_name = "home/trademark.html"
    success_url = "/trademark/"
    model = Trademark
    fields = "__all__"

    def get_queryset(self):
        return Trademark.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(TrademarkView, self).get_context_data(*args, **kwargs)
        context["text"] = TrademarkView.get_queryset(self)
        return context


# def donate_page(request):
#     """Bitcoin donation (add other crypto currencies)"""
#     content = {
#         'title': 'Support Clavem',
#         'body': 'Our hope is to have one global stable cryptocurrency that ensures transparency.',
#         'address_btc': 'public key btc',
#         'address_eth': 'public key eth'  # create Clavem's cryptocurrency wallet code
#     }
#     return render(request, 'home/donate.html', content)
