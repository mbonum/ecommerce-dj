# import os
# from mimetypes import guess_type
# from wsgiref.util import FileWrapper
# from core.utils import unique_slug_generator
# # from django.contrib.auth import authenticate, get_user_model, login, logout
from io import BytesIO
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage, send_mail
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4, landscape, letter
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfgen import canvas
from core.utils import render_to_pdf
from .models import Cookie, Donate, Page, Privacy, Terms, Trademark
# from subscribe.forms import JoinForm

Clvm = getattr(settings, "ENV_NAME", "Clavem")


class HomeView(SuccessMessageMixin, CreateView):
    # Show homepage
    template_name = "home/home.html"
    model = Page
    fields = "__all__"
    success_url = "/"

    def get_queryset(self):
        return Page.objects.all().first()

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["object"] = HomeView.get_queryset(self)
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
    # Show cookie page
    template_name = "base/txt.html"
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
    # Show privacy page
    template_name = "base/txt.html"  
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
    # Show terms page
    template_name = "base/txt.html"
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
    # Show trademark page
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


class GeneratePolicyPDF(View):
    # If there is no pdf in the database, read policy's fields and generate pdf
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        try:
            pol = Privacy.objects.get(slug=slug)
            if pol is not None:
                sec = pol.psection_set.all()
        except Privacy.DoesNotExist:
            try:
                pol = Cookie.objects.get(slug=slug)
                if pol is not None:
                    sec = pol.csection_set.all()
            except Cookie.DoesNotExist:
                try:
                    pol = Terms.objects.get(slug=slug)
                    if pol:
                        sec = pol.tsection_set.all()
                except Terms.DoesNotExist:
                    pol, sec = None
        if sec:
            p = ""
            for s in sec:
                if s.title:
                    p += "<h2>" + s.title + "</h2>"
                p += s.text
            date = pol.updated.strftime("%Y-%m-%d")
            context = {
                "title": pol.title,
                "author": "Clavem Legal Team",
                "date": date,
                "text": p,
            }
            pdf = render_to_pdf("home/policy-pdf.html", context)
            if pdf:
                response = HttpResponse(pdf, content_type="application/pdf")
                filename = f"{Clvm}_{slug}_{date}.pdf"
                content = f"inline; filename={filename}"
                download = request.GET.get("download")
                if download:
                    content = f"attachment; filename={filename}"
                response["Content-Disposition"] = content
                return response
            return HttpResponse(_("Document not found."))
        return messages.info(
            request,
            _(
                "Sorry, the text is private for now. Contact us to know when the product will be published."
            ),
        )


# def policy_pdf(request):
# reportlab
#     print(request)
#     doc = request.title
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
#     p.drawString(100, 100, doc)
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename=f"{doc}.pdf")
# download pop up

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


# def donate_page(request):
#     """Bitcoin donation (add other crypto currencies)"""
#     content = {
#         'title': 'Support Clavem',
#         'body': 'Our hope is to have one global stable cryptocurrency that ensures transparency.',
#         'address_btc': 'public key btc',
#         'address_eth': 'public key eth'  # create Clavem's cryptocurrency wallet code
#     }
#     return render(request, 'home/donate.html', content)
