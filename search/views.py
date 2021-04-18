"""
Make all apps searchable
from django.shortcuts import render
from django.db.models import Q
"""
from itertools import chain

from django.views.generic import ListView

from education.models import Book
from essays.models import Essay
from products.models import Product


class SearchView(ListView):
    template_name = "search/search-view.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)
        if query is not None:
            book_results = Book.objects.search(query=query)
            essay_results = Essay.objects.search(query=query)
            product_results = Product.objects.search(query=query)

            # combine querysets
            queryset_chain = chain(book_results, essay_results, product_results     )
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)  # since qs is a list
            return qs
        return Essay.objects.none()


class SearchProductView(ListView):
    """
    __iexact means the field is exactly this
    __icontains the field contains this
    """

    template_name = "search/search-view.html"

    def get_context_data(self, *arg, **kwargs):
        context = super(SearchProductView, self).get_context_data(*arg, **kwargs)
        context["query"] = self.request.GET.get("q")
        # query = self.request.GET.get('q') SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get("q", None)
        if query is not None:
            # lookups = Q(title__icontains=query) | Q(description__icontains=query)
            return Product.objects.search(query)  # filter(lookups).distinct()
        return Product.objects.featured()
