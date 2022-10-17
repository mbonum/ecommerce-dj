from django.conf import settings
from django.http import HttpResponseRedirect

DEFAULT_REDIRECT_URL = getattr(settings, "DEFAULT_REDIRECT_URL", "www.clavem.co")#http://


def wildcard_redirect(request, path=None):
    new_url = DEFAULT_REDIRECT_URL
    print("*** ", getattr(settings, "DEFAULT_REDIRECT_URL", "www.clavem.co"))
    if path is not None:
        new_url += "/" + path
    return HttpResponseRedirect(new_url)
