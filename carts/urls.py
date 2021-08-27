from django.urls import path
from . import views

app_name = "carts"

urlpatterns = [
    path("", views.cart_home, name="home"),
    path("add-to-cart/", views.cart_update, name="cart-update"),#api_add_to_cart, name="api-add-to-cart"),# api
    path("remove-from-cart/", views.remove_from_cart, name="remove-from-cart"),#api_remove_from_cart
    path("api/", views.cart_detail_api_view, name="api-cart"),  # YXBpL2NhcnQv/
    path("checkout/", views.checkout_home, name="checkout"),
    path("checkout/success/", views.checkout_done_view, name="success"),
    path("update/", views.cart_update, name="update"),
    # path("cartv/", views.cart_detail, name="cart"),
]
