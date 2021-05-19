import os
from mimetypes import guess_type
from wsgiref.util import FileWrapper

# from asgiref import sync_to_async

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404  # render
from django.views.generic import DetailView, ListView, View
from django.utils.translation import gettext_lazy as _

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from orders.models import ProductPurchase
from .models import Product, ProductFile


class ProductListView(ListView):
    template_name = "products/plist.html"

    def get_context_data(self, *args, **kwargs):
        # Every class-based view has this method
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().order_by("index")


# ProductFeaturedListView hide out of stock products
class DigitalProductListView(ListView):
    # Show only digital products featured
    template_name = "products/plist.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().digital()  # quantity at least >= 1


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/pdetail.html"

    def get_context_data(self, *args, **kwargs):
        # form_class = QtyForm(self.request.POST or None)
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        instance = get_object_or_404(Product, slug=slug, in_stock=True)
        instance.rangeqty
        # try:
        #     instance = Product.objects.get(slug=slug, active=True)
        # except Product.DoesNotExist:
        #     raise Http404(_("Not yet released, sorry"))
        # except Product.MultipleObjectsReturned:
        #     qs = Product.objects.filter(slug=slug, active=True)
        #     instance = qs.first()
        # except:
        #     raise Http404(_("There's a problem. We are fixing it."))
        return instance


class UserProductHistoryView(LoginRequiredMixin, ListView):
    # Account -> Digital Library
    template_name = "products/user-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=True)
        # [:3] show specific number
        return views


class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        # Permission checks
        slug = kwargs.get("slug")
        _pk = kwargs.get("pk")
        # qs = Product.objects.filter(slug=slug)
        # if qs.count() != 1:
        # raise Http404('Product not found')
        # product_obj = qs.first()
        # product_obj.get_downloads().filter(pk=_pk)
        downloads_qs = ProductFile.objects.filter(pk=_pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404(_("Product not found, sorry"))
        download_obj = downloads_qs.first()
        can_download = False
        user_ready = True
        if download_obj.user_required:
            if not request.user.is_authenticated:
                user_ready = False
        purchased_products = Product.objects.none()
        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, _("You do not have access to download this item"))
            return redirect(download_obj.get_default_url())
        fileroot = getattr(settings, "PROTECTED_ROOT")
        filepath = download_obj.file.path  # .url /media/
        final_filepath = os.path.join(fileroot, filepath)  # where the file is stored
        with open(final_filepath, "rb") as _f:
            wrapper = FileWrapper(_f)
            # content = 'some'
            mimetype = "application/force-download"  # 'text/plain' for a txt file
            # look the extension of the first [0] file
            guessed_mimetype = guess_type(filepath)[0]
            if guessed_mimetype:
                mimetype = guessed_mimetype
            response = HttpResponse(wrapper, content_type=mimetype)  # content
            response["Content-Disposition"] = f"attachment;filename={download_obj.name}"
            response["X-SendFile"] = str(download_obj.name)
            return response  # return redirect(download_obj.get_default_url())


# class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
#     queryset = Product.objects.all().featured()
#     template_name = 'products/featured_detail.html'

# class ProductDetailView(ObjectViewedMixin, DetailView):
#     template_name = 'products/p-detail.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(
#             *args, **kwargs)
#         return context

#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         _pk = self.kwargs.get('pk')
#         return Product.objects.filter(pk=_pk)
