import json
import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import LoginForm, RegisterForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from shop.models import Product
from django.utils.translation import gettext_lazy as _
from .models import Cart


STRIPE_PUB_KEY = getattr(
    settings, "STRIPE_PUB_KEY", "pk_test_8PXFWtkSVafJL52j4wfAqP2T00v1Ffpqcr"
)
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)


# def cart_detail_api_view(request):
#     cart, new_obj = Cart.objects.new_or_get(request)
#     if cart.user:
#         currency = cart.user.currency
#     else:
#         currency = "EUR"
#     products = [
#         {"id": x.id, "url": x.get_absolute_url(), "name": x.name, "price": x.price}
#         for x in cart.products.all()
#     ]
#     # if shipping add subtotal + shipment cost
#     cart_data = {
#         "products": products,
#         "currency": currency,
#         "subtotal": cart.subtotal,
#         "total": cart.total
#     }
#     return JsonResponse(cart_data)


def cart_home(request):
    cart, new_obj = Cart.objects.new_or_get(request)
    items = ""
    for p in cart.products.all():
        i = "{'id': '%s', 'name': '%s', 'price': '%s', 'quantity': '%s', 'qty_instock': '%s', 'item_total': '%s', 'img': '%s', 'url': '%s'}," % (p.id, p.name, p.price, p.order_qty, p.qty_instock, p.total_item, p.get_thumbnail(), p.get_absolute_url())
        items += i
    context = {"cart": cart, "products": items}
    return render(request, "carts/cart.html", context)


def cart_update(request):
    data = json.loads(request.body)
    product_id = data['product_id']#request.POST.get("product_id")  # update-cart.html
    update = data['update']
    quantity = data['quantity']
    print(product_id)
    # product = get_object_or_404(Product, pk=product_id)

    # product = None
    if product_id is not None:
        product = get_object_or_404(Product, id=product_id, active=True)
        # try:
        #     product = Product.objects.get(id=product_id)
        # except Product.DoesNotExist:
        #     messages.info(request, _(
        #         "Sorry, the product is not available now. Contact us to know when the product will be available."
        #     ))
    else:
        return redirect("shop:list")#cart:home

    # product_qty = int(request.POST.get("productqty")) or None input hidden
    # if product_qty is None:
    #     product_qty = 1
    # print("### ", product_qty)

    cart, new_obj = Cart.objects.new_or_get(request)
    # if not update:
    #     cart.add(product=product, quantity=1, update_quantity=False)
    # else:
    #     cart.add(product=product, quantity=quantity, update_quantity=True)
    if product in cart.products.all():
        # cart.products.remove(p)
        added = False
    else:
        cart.products.add(product)
        added = True
    cart.save()
    request.session["cart_items"] = cart.products.count()
    # return redirect(product.get_absolute_url())
    if request.is_ajax():  # Asynchronous js & XML/JSON
        json_data = {
            "added": added,
            # "removed": not added,
            # "success": True
            "cartItemCount": cart.products.count(),
        }
        return JsonResponse(json_data, status=200)
    # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    return redirect("shop:list")#cart:home


def remove_from_cart(request):
    #api_remove_from_cart data = json.loads(request.body)
    # json_data = {"success": True}
    # product_id = str(data["product_id"])
    # cart = Cart(request)
    # cart.remove(product_id)
    product_id = request.POST.get("product_id")
    product = None
    if product_id is not None:
        product = Product.objects.get(id=product_id)
#from django.core.exceptions import ObjectDoesNotExist try: except ObjectDoesNotExist: messages.error(request, "No product")return redirect("")#raise
        #except Product.DoesNotExist:
    else:
        messages.info(request, _(
            "Sorry, the product is not available now. Contact us to know when the product will be available."            ))
        return redirect("cart:home")
    cart, new_obj = Cart.objects.new_or_get(request)
    if product in cart.products.all():
        cart.products.remove(product)
        cart.save()
        request.session["cart_items"] = cart.products.count()
    return JsonResponse(json_data)


def checkout_home(request):
    cart, new_obj = Cart.objects.new_or_get(request)
    order = None
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
    order, order_created = Order.objects.new_or_get(billing_profile, cart)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order, order_created = Order.objects.new_or_get(
            billing_profile, cart
        )
        if shipping_address_id:
            order.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order.save()
        has_card = billing_profile.has_card
    if request.method == "POST":  # check that order is done
        if order is not None:
            is_prepared = order.check_done()
            if is_prepared:
                did_charge, crg_msg = billing_profile.charge(order)
                if did_charge:
                    order.mark_paid()
                    request.session["cart_items"] = 0
                    del request.session["cart_id"]
                    if not billing_profile.user:
                        billing_profile.set_cards_inactive()
                    return redirect("cart:success")
                else:
                    return redirect("cart:checkout")
    context = {
        "object": order,
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
    # cart = Cart.objects.get(request)#new_or_get
    # cart.clear()
    return render(request, "carts/checkout-done.html", {})
