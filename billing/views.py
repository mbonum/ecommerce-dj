import stripe
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url

from .models import (
    BillingProfile,
    Card,
    STRIPE_SECRET_KEY,
    STRIPE_PUB_KEY,
)  # , CardManager

STRIPE_SECRET_KEY = STRIPE_SECRET_KEY
STRIPE_PUB_KEY = STRIPE_PUB_KEY
stripe.api_key = STRIPE_SECRET_KEY


def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request
    )
    # if request.user.is_authenticated:
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id
    if not billing_profile:
        return redirect("cart:home")
    next_ = request.GET.get("next")
    next_url = None
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(
        request,
        "billing/payment-method.html",
        {"publish_key": STRIPE_PUB_KEY, "next_url": next_url},
    )


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            request
        )
        if not billing_profile:
            return HttpResponse({"message": " Please add your card."}, status_code=401)

        # check aproject.main.js function stripeTokenHandler
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
        return JsonResponse({"message": "Great! Your card was added. Thank you!"})
    return HttpResponse({"message": " Please add your card."}, status_code=401)
