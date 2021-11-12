from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from education.models import Book
from essays.models import Essay
from shop.models import Category, Product
from team.models import Member


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            "learn:booklist",
            "read:index",
            "shop:list",
        ]

    def location(self, item):
        return reverse(item)


class BookSitemap(Sitemap):
    def items(self):
        return Book.objects.all()


class EssaySitemap(Sitemap):
    # changefreq = "weekly"
    # priority = 0.8

    def items(self):
        return Essay.objects.all()

    def lastmod(self, obj):
        return obj.updated


class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()


class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated


class TeamSitemap(Sitemap):
    def items(self):
        return Member.objects.all()