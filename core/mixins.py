from django.utils.http import url_has_allowed_host_and_scheme


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class NextUrlMixin(object):
    # Redirect to checkout

    default_next = "/"

    def get_next_url(self):
        request = self.request
        next_ = request.GET.get("next")
        next_post = request.POST.get("next")
        redirect_path = next_ or next_post or None
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next
