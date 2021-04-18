from django.contrib import admin
from django.forms import ModelForm
# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from .models import Order, ProductPurchase


# class OrderModelForm(ModelForm):
#     class Meta:
#         model = Order
#         exclude = ()
#         widgets = {
#             "active": DjangoToggleSwitchWidget(
#                 round=True, klass="django-toggle-switch-success"
#             ),
#         }


class OrderAdmin(admin.ModelAdmin):
    # form = OrderModelForm
    list_display = ("order_id", "billing_profile", "created_at")
    list_filter = ("created_at",)


admin.site.register(Order, OrderAdmin)
admin.site.register(ProductPurchase)
