# pip install readtime
from django import template
import readtime

register = template.Library()


def read(html):
    return readtime.of_html(html)


# def read_tot(readtime):
#     t += readtime
#     return t


register.filter("readtime", read)
