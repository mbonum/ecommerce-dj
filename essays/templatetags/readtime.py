# pip install readtime
from django.template import Library
import readtime

register = Library()

# @register.filter()
def read(html):
    return readtime.of_html(html)


# def read_tot(readtime):
#     t += readtime
#     return t


register.filter("readtime", read)
