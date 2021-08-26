# import json
import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from accounts.forms import LoginForm, RegisterForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from shop.models import Product
from django.utils.translation import gettext_lazy as _
from .cart import Cart as C
from .models import Cart


STRIPE_PUB_KEY = getattr(
    settings, "STRIPE_PUB_KEY", "pk_test_8PXFWtkSVafJL52j4wfAqP2T00v1Ffpqcr"
)
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)


def cart_detail(request):# Vue cartv
    cart = C(request)
    products = ""
    for i in cart:
        p = i["product"]
        #url = f"/shop/{product.category.slug}/{product.slug}/"# fix
        product = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'url': '%s', 'num_available': '%s'}," % (p.id, p.title, p.price, i['quantity'], i['total_price'], p.get_thumbnail(), p.get_absolute_url(), p.num_available)
        products += product
    context = {"cart": cart, "products": products}
    return render(request, "carts/cart.html", context)


def cart_detail_api_view(request):
    cart, new_obj = Cart.objects.new_or_get(request)
    if cart.user:
        currency = cart.user.currency
    else:
        currency = "EUR"
    products = [
        {"id": x.id, "url": x.get_absolute_url(), "name": x.name, "price": x.price}
        for x in cart.products.all()
    ]
    # if shipping add subtotal + shipment cost
    cart_data = {
        "products": products,
        "currency": currency,
        "subtotal": cart.subtotal,
        "total": cart.total,
    }
    return JsonResponse(cart_data)


def cart_home(request):
    cart, new_obj = Cart.objects.new_or_get(request)
    products = ""
    for i in cart.products.all():
        p = "{'id': '%s', 'name': '%s', 'price': '%s', 'quantity': '%s', 'qty_instock': '%s', 'item_total': '%s', 'img': '%s', 'url': '%s'}," % (i.id, i.name, i.price, i.order_qty, i.qty_instock, i.total_item, i.get_thumbnail(), i.get_absolute_url())#f'{{"id": "{i.id}", "name": "{i.name}", "price": "{i.price}", "quantity": "{i.qty_instock}", "url": "{i.get_absolute_url()}", "img": "{i.thumbnail.url}"}},}}'
        products += p
    context = {"cart": cart, "products": products}
    return render(request, "carts/cart-home.html", context)


def cart_update(request):#def api_add_to_cart(request):
#     data = json.loads(request.body)
#     jsonresponse = {'success': True}
#     product_id = data['product_id']
#     update = data['update']
#     quantity = data['quantity']
#     if product_id is not None:
#         try:
#             product = Product.objects.get(id=product_id)
# #from django.core.exceptions import ObjectDoesNotExist try: except ObjectDoesNotExist: messages.error(request, "No product")return redirect("")#raise
#         except Product.DoesNotExist:
#             messages.info(request, _(
#                 "Sorry, the product is not available now. Contact us to know when the product will be available."
#             ))
#             return redirect("shop:list")#cart:home
#     cart, new_obj = Cart.objects.new_or_get(request)
#     # product = get_object_or_404(Product, pk=product_id)
#     if product in cart.products.all():
#         cart.products.remove(product)
#         added = False
#     else:
#         cart.products.add(product)
#         added = True
#     request.session["cart_items"] = cart.products.count()# return redirect(product.get_absolute_url())
#     if request.is_ajax():  # Asynchronous js & XML/JSON
#         json_data = {
#             "added": added,
#             "removed": not added,
#             "cartItemCount": cart.products.count(),
#         }
#         return JsonResponse(json_data, status=200)# return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
#     return redirect("shop:list")

    product_id = request.POST.get("product_id")  # update-cart.html
    if product_id is not None:
        try:
            product = Product.objects.get(id=product_id)
        #from django.core.exceptions import ObjectDoesNotExist try: except ObjectDoesNotExist: messages.error(request, "No product")return redirect("")#raise
        except Product.DoesNotExist:
            messages.info(request, _(
                "Sorry, the product is not available now. Contact us to know when the product will be available."
            ))
            return redirect("shop:list")#cart:home

        # product_qty = int(request.POST.get("productqty")) or None input hidden
        # if product_qty is None:
        #     product_qty = 1
        # print("### ", product_qty)

        cart, new_obj = Cart.objects.new_or_get(request)
        if product in cart.products.all():
            cart.products.remove(product)
            added = False
        else:
            cart.products.add(product)
            added = True
        request.session["cart_items"] = cart.products.count()
        # return redirect(product.get_absolute_url())
        if request.is_ajax():  # Asynchronous js & XML/JSON
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart.products.count(),
            }
            return JsonResponse(json_data, status=200)
    # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    return redirect("shop:list")#cart:home


def checkout_home(request):
    cart, new_obj = Cart.objects.new_or_get(request)
    order_obj = None
    if new_obj or cart.products.count() == 0:
        return redirect("cart:home")
    login_form = LoginForm(request=request)
    register_form = RegisterForm
    address_form = AddressForm
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_required = not cart.is_digital
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request
    )
    order_obj, order_created = Order.objects.new_or_get(billing_profile, cart)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile, cart
        )
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card
    if request.method == "POST":  # check that order is done
        if order_obj is not None:
            is_prepared = order_obj.check_done()
            if is_prepared:
                did_charge, crg_msg = billing_profile.charge(order_obj)
                if did_charge:
                    order_obj.mark_paid()
                    request.session["cart_items"] = 0
                    del request.session["cart_id"]
                    if not billing_profile.user:
                        billing_profile.set_cards_inactive()
                    return redirect("cart:success")
                else:
                    return redirect("cart:checkout")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "register_form": register_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
        "shipping_address_required": shipping_address_required,
    }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
