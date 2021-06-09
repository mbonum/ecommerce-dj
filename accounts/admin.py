from django.contrib import admin

# from django.contrib.admin.views.decorators import staff_member_required ## https://django-allauth-2fa.readthedocs.io/en/latest/installation/

# # Ensure users go through the allauth workflow when logging into admin.
# admin.site.login = staff_member_required(admin.site.login, login_url='/bmltZGEtbWdiLTI1Cg/login')#/accounts/login
# # Run the standard admin set-up.
# admin.autodiscover()

from django.contrib.auth import get_user_model

# from django.contrib.auth.models import Group
# from django.forms import ModelForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import EmailActivation

USER = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ("email", "is_superuser", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_superuser", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "first_name", "password", "currency")}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),  # 'is_superuser',
        ("Personal", {"fields": ("bio",)}),
    )
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password")}),)
    # formfield_overrides = {
    #     USER.bio: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    # }
    search_fields = ("email", "first_name")
    ordering = ["-date_joined"]
    filter_horizontal = ()


class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ("email",)

    class Meta:
        model = EmailActivation


admin.site.register(USER, UserAdmin)
admin.site.register(EmailActivation, EmailActivationAdmin)
