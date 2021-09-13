from django.urls import path
from . import views

app_name = "carts"

urlpatterns = [
    path("", views.cart_home, name="home"),
    path("update/", views.cart_update, name="update-cart"),
    path("remove-from-cart/", views.remove_from_cart, name="remove-from-cart"),
    # path("api/", views.cart_detail_api_view, name="api-cart"),  # vanilla js YXBpL2NhcnQv/
    path("checkout/", views.checkout_home, name="checkout"),
    path("checkout/success/", views.checkout_done_view, name="success")
]
