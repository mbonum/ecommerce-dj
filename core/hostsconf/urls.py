from django.urls import include, path, re_path

from .views import wildcard_redirect

urls_patterns = [
    re_path(r"^(?P<path>.*)", wildcard_redirect),
]
