from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

# from .models import Essay


class EssaySitemap(Sitemap):
    """
    Add essay list to sitemap.xml
    """

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["essays:index"]  # Essay.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated

    def location(self, item):
        return reverse(item)
