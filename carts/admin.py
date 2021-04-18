from django.contrib import admin

# from django.forms import ModelForm
# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

from .models import Cart


# class CartModelForm(ModelForm):
#     class Meta:
#         model = Cart
#         exclude = ()
#         widgets = {
#             'active': DjangoToggleSwitchWidget(round=True, klass='django-toggle-switch-success'),
#         }


class CartAdmin(admin.ModelAdmin):
    # form = CartModelForm
    list_display = (
        "user",
        "total",
        "created_at",
    )
    list_filter = ("created_at",)


admin.site.register(Cart, CartAdmin)
