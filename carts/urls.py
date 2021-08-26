from django.urls import path

from . import views

app_name = "carts"

urlpatterns = [
    path("", views.cart_home, name="home"),
    path("cartv/", views.cart_detail, name="cart"),
    path("checkout/", views.checkout_home, name="checkout"),
    path("checkout/success/", views.checkout_done_view, name="success"),
    path("update/", views.cart_update, name="update"),
]
