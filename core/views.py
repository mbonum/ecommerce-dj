from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    """
    robots.txt is a standard text file that tells search engine crawlers which pages they can access, scrape, and ultimately list in their search engine results.
    """
    lines = [
        "User-Agent: *",  # Googlebot Bingbot Slurp
        # "Disallow: /private/",
        "Disallow: /bmltZGEtbWdiLTI1Cg",  # admin
        "Disallow: /c",
        # "Disallow: /bmltZGEtbWdiLTI1Cg/defender",
        "Disallow: /media/protected/",  # /*.xls$
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
