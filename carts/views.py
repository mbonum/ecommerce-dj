import json
import stripe
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from accounts.forms import LoginForm, RegisterForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from shop.models import Product
from .models import Cart


STRIPE_PUB_KEY = getattr(
    settings, "STRIPE_PUB_KEY", "pk_test_8PXFWtkSVafJL52j4wfAqP2T00v1Ffpqcr"
)
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)


def cart_home(request):
    # Show cart page
    cart, new_obj = Cart.objects.new_or_get(request)
    items = ""
    shipping = 0.00
    for p in cart.products.all():
        i = "{'id': '%s', 'name': '%s', 'price': '%s', 'qty': '%s', 'qty_instock': '%s', 'item_total': '%s', 'img': '%s', 'url': '%s'}," % (p.id, p.name, p.price, p.order_qty, p.qty_instock, p.total_item, p.get_thumbnail(), p.get_absolute_url())
        items += i
        # print("$$$", p.is_digital)
        # To determine the shipping cost and tax we need to know the address.
        # Show shipping cost if the shipping address is verified.
        # if not p.is_digital:
        #     shipping = float("%.2f" % (9.99))
        # , "shipping_cost": shipping
    context = {"cart": cart, "products": items}
    return render(request, "carts/cart.html", context)


def cart_update(request):
    # Add product to cart if user clicks on Add to Cart button in the product detail page
    data = json.loads(request.body)
    # vue update-cart.html
    product_id = data['product_id']
    update = data['update']
    qty = int(data['qty'])
    # product = None
    if product_id is not None:
        try:
            product = Product.objects.get(id=product_id, active=True)
        except Product.DoesNotExist:
            messages.info(request, _(
                "Sorry, the product is not available now. Contact us to know when the product will be available."
            ))
    else:
        return redirect("shop:list")
    cart, new_obj = Cart.objects.new_or_get(request)
    if update: # product in cart.products.all():
        # cart.products.remove(product)
        # Cart button Add qty.
        added = False
        cart.update_order_qty(product_id, qty)
    else:
        # Product detail button Add to cart.
        added = True
        # if not product.is_digital:
        #     request.session["shipping"] = True
        # Add qty btn in product detail
        # product.order_qty = qty
        cart.products.add(product)
        # request.session["cart_items"] += 1
    request.session["cart_items"] = cart.nr_items()
    cart.save()

    if request.accepts("application/json"):# is_ajax depreciated
        json_data = {
            "added": added,
            # "shipping": request.session["shipping"],
            "success": True,
            "cartItemCount": request.session["cart_items"],
        }
        return JsonResponse(json_data, status=200)
    # JsonResponse({"message": "Error 400"}, status=400)
    return redirect("shop:list")


def remove_from_cart(request):
    # Remove product from cart if user click on the X button in the cart page
    
    data = json.loads(request.body)
    product_id = int(data['product_id'])
    if product_id is not None:
        try:
            product = Product.objects.get(id=product_id, active=True)
        except Product.DoesNotExist:
            messages.info(request, _(
                "Sorry, the product is not available now. Contact us to know when the product will be available."
            ))
            return redirect("shop:list")
    else:
        return redirect("shop:list")

    cart, new_obj = Cart.objects.new_or_get(request)
    if product in cart.products.all():
        cart.products.remove(product)
        cart.save()
        request.session["cart_items"] = cart.nr_items()
    json_data = {"success": True}
    return JsonResponse(json_data)


def checkout_home(request):
    cart, new_obj = Cart.objects.new_or_get(request)
    order = None
    if new_obj or cart.products.count() == 0:
        return redirect("shop:list")
    login_form = LoginForm(request=request)
    register_form = RegisterForm
    address_form = AddressForm
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_required = False
    for p in cart.products.all():
        if not p.is_digital:
            shipping_address_required = True
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
        # order, order_created = Order.objects.new_or_get(
        #     billing_profile, cart
        # )
        if shipping_address_id:
            order.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order.save()
        has_card = billing_profile.has_card
    # Check whether the order is done
    if request.method == "POST":
        if order is not None:
            is_prepared = order.check_done()
            if is_prepared:
                did_charge, crg_msg = billing_profile.charge(order)
                if did_charge:
                    order.mark_paid()
                    # cart.clear()
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
    # cart, new_obj = Cart.objects.new_or_get(request)
    # c = get_object_or_404(Cart, slug=slug)
    # o = c.products.all()
    # context = {"order_id": order.order_id,}
    # return render(request, "shop/category.html", context)
    # # cart = Cart.objects.new_or_get(request)
    # # order = Order.objects.get(cart=cart)
    # # # cart.clear()
    # # email_body = render_to_string("order-email.html", context)
    return render(request, "carts/checkout-done.html", {})


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