# from django.shortcuts import render
from core.utils import render_to_pdf
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, JsonResponse

# from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, View

# from billing.models import BillingProfile
from .models import Order, ProductPurchase

# templatetags.py
# from django.template import Library
# from core.models import Order

# register = Library()


# @register.filter
# def cart_item_count(user):
#     if user.is_authenticated:
#         qs = Order.objects.filter(user=user, ordered=False)
#         if qs.exists():
#             return qs[0].items.count()
#     return 0

class OrderListView(LoginRequiredMixin, ListView):
    template_name = "orders/olist.html"

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/odetail.html"

    def get_object(self):
        qs = Order.objects.by_request(self.request).filter(
            order_id=self.kwargs.get("order_id")
        )
        if qs.count() == 1:
            return qs.first()
        return Http404(
            _(
                "Apologies, order not found, please retry. If the problem persists please contact us."
            )
        )


class LibraryView(LoginRequiredMixin, ListView):
    template_name = "orders/library.html"

    def get_queryset(self):
        return ProductPurchase.objects.products_by_request(self.request)  # .digital()


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            product_id = data.get("product_id", None)
            if product_id is not None:
                product_id = int(product_id)
                ownership_ids = ProductPurchase.objects.products_by_id(request)
                if product_id in ownership_ids:
                    return JsonResponse({"owner": True})
                return JsonResponse({"owner": False})
        raise Http404(
            _(
                "Apologies, nothing found, please retry. If the problem persists please contact us."
            )
        )


class GenerateOrderPDF(View):
    def get(self, request, *args, **kwargs):
        # template = get_template('order/pdf/invoice.html')
        order_id = self.kwargs.get("_id")  # core/urls order-detail.html
        order = Order.objects.get(order_id=order_id)
        customer_first = order.cart.user.first_name
        customer_last = order.cart.user.last_name
        customer = customer_first
        if customer_last:
            customer += " " + customer_last
        customer_email = order.cart.user.email
        # customer_id = order.billing_profile.customer_id
        billing_address = (
            order.billing_address.street
            + ", "
            + order.billing_address.city
            + ", "
            + order.billing_address.state
            + ", "
            + order.billing_address.postal_code
            + ", "
            + order.billing_address.country
        )
        if order.shipping_address:
            shipping_address = (
                order.shipping_address.street
                + ", "
                + order.shipping_address.city
                + ", "
                + order.shipping_address.state
                + ", "
                + order.shipping_address.postal_code
                + ", "
                + order.shipping_address.country
            )
            shipping_total = order.shipping_total
        cart = [
            {
                "id": p.id,
                "url": p.get_absolute_url(),
                "name": p.name,
                "type": p.get_product_type_display,
                "price": p.price,
            }
            for p in order.cart.products.all()
        ]
        # qty = order.cart.user_qty#products.quantity
        currency = order.cart.user.currency
        total = order.total
        date = order.updated_at
        context = {
            "order_id": order_id,
            "customer": customer,
            "customer_email": customer_email,
            "cart": cart,
            "billing_address": billing_address,
            "shipping_address": shipping_address,
            "shipping_total": shipping_total,
            "currency": currency,
            "total": total,
            "date": date,
        }
        # html = template.render(context)
        pdf = render_to_pdf("orders/pdf/invoice.html", context)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            url = getattr(settings, "BASE_URL")
            filename = f"{url}_invoice-order-{order_id}.pdf"
            content = f"inline; filename={filename}"
            download = request.GET.get("download")
            if download:
                content = f"attachment; filename={filename}"
            response["Content-Disposition"] = content
            return response
        raise Http404(#HttpResponse
            _(
                "Apologies, document not found, please retry. If the problem persists please contact us."
            )
        )
