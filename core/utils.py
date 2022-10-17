import datetime
import os  # import re
import random
import string
from base64 import b64decode
from io import BytesIO
import six
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.text import slugify
from PIL import Image
from xhtml2pdf import pisa

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)


def find_string(filename, string: str):
    f = open(filename, "r")
    temp = False
    if string in f.read():
        temp = True
    return temp
    # w = raw_input("Input the English word: ")

    # open the file using `with` context manager, it'll automatically close the file for you
    # with open("temp-emails.txt") as f:
    #     temp = False
    #     for domain in f:  # iterate over the file one line at a time(memory efficient)
    #         if re.search(f"\b{email}\b", line):
    #             temp = True
    #     if not found:
    #         print("The translation cannot be found!")


def code_gen(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.digits):
    # Shorturl
    return "".join(random.choice(chars) for _ in range(size))
    # shortcut of a = '' for _ in range(): a += random.choice(chars) return a


def create_shortcode(instance, size=SHORTCODE_MIN):
    new = code_gen(size=size)
    clurl = instance.__class__
    qs = clurl.objects.filter(shortcode=new).exists()
    if qs:
        return create_shortcode(size=size)
    return new


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


# def decode_base64_image(data):
#     try:
#         data = b64decode(data.encode('UTF-8'))
#         buf = BytesIO(data)
#         img = Image.open(buf)
#         return img
#     except:
#         return None


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    # Return random strings to naming files
    return "".join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    # Return random keys
    size = random.randint(30, 60)
    key = random_string_generator(size)
    # size = randint(30, 60)
    # key = random_string_generator(size=size)
    # qs = EmailActivation.objects.filter(key__iexact=key)
    # if qs.exists():
    #     key = random_string_generator(size=size)
    klass = instance.__class__
    qs_exists = klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_key_generator(instance)
    return key


def unique_order_id_generator(instance):
    # Return random order IDs, e.g. 69MF5CYBCK
    order_new_id = random_string_generator().upper()  # to generate capital Letters
    klass = instance.__class__
    qs_exists = klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    # This assumes your instance has a model with a slug field and a title CharField
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def render_to_pdf(template_src, context_dict=None):  # {}
    # Generate a pdf from an html page
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # , link_callback=link_callback
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF8")), result)
    if not pdf.err:
        return (
            result.getvalue()
        )  # HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def get_last_month_data(today):
    # Simple method to get the datetime objects for the start and end of last month
    this_month_start = datetime.datetime(today.year, today.month, 1)
    last_month_end = this_month_start - datetime.timedelta(days=1)
    last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
    return (last_month_start, last_month_end)


def get_month_data_range(months_ago=1, include_this_month=False):
    # Generate a list of dictionaires that describe any given amout of monthly data
    today = datetime.datetime.now().today()
    dates = []
    if include_this_month:
        # get next month's data
        next_month = today.replace(day=28) + datetime.timedelta(days=4)
        # use next month's data to get this month's data breakdown
        start, end = get_last_month_data(next_month)
        dates.insert(
            0,
            {
                "start": start.timestamp(),
                "end": end.timestamp(),
                "start_json": start.isoformat(),
                "end_json": end.isoformat(),
                "timesince": 0,
                "year": start.year,
                "month": str(start.strftime("%B")),
            },
        )
    for _ in range(0, months_ago):
        start, end = get_last_month_data(today)
        today = start
        dates.insert(
            0,
            {
                "start": start.timestamp(),
                "start_json": start.isoformat(),
                "end": end.timestamp(),
                "end_json": end.isoformat(),
                "timesince": int((datetime.datetime.now() - end).total_seconds()),
                "year": start.year,
                "month": str(start.strftime("%B")),
            },
        )
    return dates  # dates.reverse()


def get_filename(path):
    return os.path.basename(path)


# from django.utils import timezone
# from core import settings
# xhtml2pdf doesn't render images
# def link_callback(uri):
#     ''', rel Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources'''
#     surl = settings.STATIC_URL # /static/
#     sroot = settings.STATIC_ROOT
#     murl = settings.MEDIA_URL
#     mroot = settings.MEDIA_ROOT
#     # convert URIs to absolute system paths
#     if uri.startswith(murl):
#         path = os.path.join(mroot, uri.replace(murl, ""))
#     elif uri.startswith(surl):
#         path = os.path.join(sroot, uri.replace(surl, ""))
#     else:
#         return uri # handle absolute uri, i.e. http://some.tld/foo.png
#     # make sure that file exists
#     if not os.path.isfile(path):
#         raise Exception(
#             'media URI must start with %s or %s' % (surl, murl)
#         )
#     return path
