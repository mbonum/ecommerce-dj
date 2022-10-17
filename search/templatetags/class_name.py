from django.template import Library

register = Library()


# @register.filter()
def class_name(value):
    return value.__class__.__name__


register.filter("class_name", class_name)
