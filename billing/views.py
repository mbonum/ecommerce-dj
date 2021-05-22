import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from django.utils.translation import gettext_lazy as _

from .models import BillingProfile, Card  # , CardManager

# getattr(settings, "STRIPE_SECRET_KEY", "sk_test_SY6ETmVlRlazamotRhz8pS7p00PDpyHd5l")
# STRIPE_PUB_KEY = getattr(
#     settings, "STRIPE_PUB_KEY", "pk_test_8PXFWtkSVafJL52j4wfAqP2T00v1Ffpqcr"
# )
stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request
    )
    # print("*** ", settings.STRIPE_PUB_KEY, billing_profile)
    # if request.user.is_authenticated:
    #     billing_profile = request.user.billingprofile
    #     customer_id = billing_profile.customer_id
    if not billing_profile:
        return redirect("cart:home")
    next_url = None
    next_ = request.GET.get("next")
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(
        request,
        "billing/payment-method.html",
        {"publish_key": settings.STRIPE_PUB_KEY, "next_url": next_url},
    )


def payment_method_createview(request):
    msg = _(" Please add your card.")
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            request
        )
        if not billing_profile:
            return HttpResponse(
                msg, status=401
            )  # {"message": msg}"message": "Cannot find this user"}

        # cdev.stripe.js function stripeTokenHandler
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
        return JsonResponse(
            {"message": _("Great! Your card has been added. Thank you!")}
        )
    return HttpResponse(msg, status=401)  # "error" {"message": msg}
