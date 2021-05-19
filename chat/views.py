import stripe
from django.conf import settings
from django.shortcuts import render


# from django.views import View
# from django.http import JsonResponse
# from django.views.generic import TemplateView
from .models import Message

stripe.api_key = settings.STRIPE_SECRET_KEY


def room(request, room):
    name = request.GET.get("username", "You")
    messages = Message.objects.filter(room=room)[0:25]
    return render(
        request,
        "chat/room.html",
        {"room": room, "username": name, "messages": messages},
    )


# class Success(TemplateView):
#     template_name = "chat/success.html"


# class Checkpage(TemplateView):
#     template_name = "chat/check.html"

#     def get_context_data(self, **kwargs):
#         # product = Product.objects.get(name="test")
#         context = super(Checkpage, self).get_context_data(**kwargs)
#         context.update({"STRIPE_PUB_KEY": settings.STRIPE_PUB_KEY})
#         return context


# class Checkout(View):
#     def post(self, request, *args, **kwargs):
#         # product_slug = self.kwargs["slug"]
#         # product = Product.objects.get(slug=product_slug)
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "unit_amount": 2000,# product.price
#                         "product_data": {
#                             "name": "Stubborn Attachments",# product.name
#                             # 'images': ['https://i.imgur.com/EHyR2nP.png'],
#                         },
#                     },
#                     "quantity": 1,
#                 },
#             ],
#             mode="payment",
#             success_url="/success/",
#             cancel_url="/cancel/",
#         )
#         return JsonResponse({"id": checkout_session.id})
