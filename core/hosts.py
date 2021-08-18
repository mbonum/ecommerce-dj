from django.conf import settings
from django_hosts import host, patterns


ROOT_URLCONF = getattr(settings, "ROOT_URLCONF", "core.urls")

host_patterns = patterns(
    "",
    host(r"www", ROOT_URLCONF, name="www"),
    # # clavem
    host(r"(?!www)\w+", "core.hostsconf.urls", name="wildcard"),
    # .*
    # host(r"docs", "docs.urls", name="docs"),  # global docs
    host(r"read", "apps.essays.urls", name="read"),
    host(r"shop", "apps.shop.urls", name="shop"),
    # host(r"dome", "apps.dome.urls", name="dome"),  # clvm house
    # host(r"dose", "apps.dose.urls", name="dose"),  # clvm dosing
    # host(r"learn", "apps.education.urls", name="learn"),
    # host(r'admin', 'urls.admin', name='admin', scheme='https://'),
    # host(r'beta', 'beta.urls', name='beta'),
)
