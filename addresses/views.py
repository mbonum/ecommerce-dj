from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

# from settings.logger import logger

from billing.models import BillingProfile

from .forms import AddressForm
from .models import Address


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    next_ = request.GET.get("next")
    next_post = request.POST.get("next", None)
    redirect_path = next_ or next_post or None

    # logger.debug(f"Check redirect {next}")

    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            request
        )
        if billing_profile is not None:
            address_type = request.POST.get(
                "address_type", "billing"
            )
            instance.billing_profile = billing_profile or "billing"
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
        else:
            return redirect("cart:checkout")
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("cart:checkout")


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None
        if request.method == "POST":
            shipping_address = request.POST.get("shipping_address", None)
            address_type = request.POST.get("address_type", "shipping")
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(
                    billing_profile=billing_profile, id=shipping_address
                )
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
                if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("cart:checkout")


class AddressListView(LoginRequiredMixin, ListView):
    template_name = "addresses/list.html"

    def get_queryset(self):
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            self.request
        )
        return Address.objects.filter(billing_profile=billing_profile)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "addresses/update.html"
    form_class = AddressForm
    success_url = "/addresses/"

    def get_queryset(self):
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            self.request
        )
        return Address.objects.filter(billing_profile=billing_profile)


class AddressCreateView(LoginRequiredMixin, CreateView):
    template_name = "addresses/update.html"
    form_class = AddressForm
    success_url = "/addresses/"

    def form_valid(self, form):
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            self.request
        )
        instance = form.save(commit=False)
        instance.billing_profile = billing_profile
        instance.save()
        return super(AddressCreateView, self).form_valid(form)

    # def get_queryset(self):
    #     return Address.objects.filter(billing_profile=billing_profile)