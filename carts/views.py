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
from products.models import Product
from django.utils.translation import gettext_lazy as _

from .models import Cart


STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", None)
STRIPE_PUB_KEY = getattr(
    settings, "settings.STRIPE_PUB_KEY", "pk_test_8PXFWtkSVafJL52j4wfAqP2T00v1Ffpqcr"
)
stripe.api_key = STRIPE_SECRET_KEY


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj.user:
        currency = cart_obj.user.currency
    else:
        currency = "EUR"
    products = [
        {"id": x.id, "url": x.get_absolute_url(), "name": x.name, "price": x.price}
        for x in cart_obj.products.all()
    ]
    # if shipping add subtotal + shipment cost
    cart_data = {
        "products": products,
        "currency": currency,
        "subtotal": cart_obj.subtotal,
        "total": cart_obj.total,
    }
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/cart-home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get("product_id")
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            msg = _(
                "Sorry, the product is not available at the moment."
                "Contact us to know when the product will be available."
            )
            messages.success(request, msg)
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)  # product_id
            added = True
        request.session["cart_items"] = cart_obj.products.count()
        # return redirect(product_obj.get_absolute_url())
        if request.is_ajax():  # Asynchronous Javascript and XML / JSON
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count(),
            }
            return JsonResponse(json_data, status=200)
    # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    # order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    user = request.user
    login_form = LoginForm(request=request)
    register_form = RegisterForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id_required = not cart_obj.is_digital
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request
    )
    order_obj, order_created = Order.objects.new_or_get(billing_profile, cart_obj)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile, cart_obj
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
    if request.method == "POST":  # 'check that order is done'
        # if order_obj is not None:
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()  # like a signal
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
        # 'billing_address_form': billing_address_form,# if you change address_form
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
        "shipping_address_id_required": shipping_address_id_required,
    }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    """Show Thank you page and send email"""
    return render(request, "carts/checkout-done.html", {})


# import os
# from flask import Flask, jsonify, request
# import stripe

## This is your test secret API key.

# stripe.api_key = 'sk_test_SY6ETmVlRlazamotRhz8pS7p00PDpyHd5l'

# app = Flask(__name__, static_url_path='', static_folder='.')

# YOUR_DOMAIN = 'http://localhost:4242'

# @app.route('/create-checkout-session', methods=['POST'])

# def create_checkout_session():
#     try:
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'usd',
#                         'unit_amount': 2000,
#                         'product_data': {
#                             'name': 'Stubborn Attachments',
#                             'images': ['https://i.imgur.com/EHyR2nP.png'],
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success.html',
#             cancel_url=YOUR_DOMAIN + '/cancel.html',
#         )
#         return jsonify({'id': checkout_session.id})
#     except Exception as e:
#         return jsonify(error=str(e)), 403

# if __name__ == '__main__':
#     app.run(port=4242)
