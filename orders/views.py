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


class OrderListView(LoginRequiredMixin, ListView):
    template_name = "orders/order-list.html"

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/order-detail.html"

    def get_object(self):
        # _id = self.kwargs.get('order_id')
        qs = Order.objects.by_request(self.request).filter(
            order_id=self.kwargs.get("order_id")
        )
        # print(_id)
        if qs.count() == 1:
            return qs.first()
        return Http404(
            _(
                "Order not found, please try again. If the problem persists please contact us."
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
        raise Http404("Not found, sorry")


class GenerateOrderPDF(View):
    def get(self, request, *args, **kwargs):
        # template = get_template('order/pdf/invoice.html')
        order_id = self.kwargs.get("_id")  # core/urls order-detail.html
        order = Order.objects.get(order_id=order_id)
        customer_first = order.cart.user.first_name
        customer_last = order.cart.user.last_name
        customer = customer_first + " " + customer_last
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
        # shipping_address = order.shipping_address.street
        cart = [
            {"id": x.id, "url": x.get_absolute_url(), "name": x.name, "price": x.price}
            for x in order.cart.products.all()
        ]
        # qty = order.cart.user_qty#products.quantity
        currency = order.cart.user.currency
        total = order.total
        date = order.updated
        context = {
            "order_id": order_id,
            "customer": customer,
            "customer_email": customer_email,
            "billing_address": billing_address,
            # 'shipping_address': shipping_address,
            "cart": cart[0],
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
        return HttpResponse("Document not found.")


# class GenerateOrderPDF(View):
#     def get(self, *args, **kwargs):
#         template = get_template('pdf/invoice.html')
#         order_id = kwargs.get("pk")
#         order = Order.objects.get(id=order_id)
#         # print(essay.image)
#         context = {
#             'title': order.title,
#             'author': order.author,
#             'date': order.updated,
#             'body': order.body,
#             'image': order.image
#         }
#         html = template.render(context)
#         # pypandoc.convert_file(html)
#         pdf = render_to_pdf('pdf/invoice.html', context)
#         return pdf
# function-based view
# def generate_view(request, *args, **kwargs):
#     template = get_template('pdf/invoice.html')
#     context = {
#         'invoice_id': 123,
#         'customer_name': 'MkB',
#         'amount': 123.50,
#         'today': '12/12/18'
#     }
#     html = template.render(context)
#     return HttpResponse(html)
