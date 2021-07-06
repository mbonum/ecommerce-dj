# from django.utils.http import is_safe_url from django_registration.forms import RegistrationForm
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV3#, ReCaptchaV2Checkbox
from captcha.fields import CaptchaField, CaptchaTextInput
from disposable_email_checker.validators import validate_disposable_email
from django import forms
from django.conf import settings
from django.contrib.auth import (
    authenticate,
    password_validation,
    get_user_model,
    login,
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import EmailActivation  # , CustomUser
from .signals import USER_LOGGED_IN

USER = get_user_model()

# HCAPTCHA_SECRET_KEY = getattr(settings, "HCAPTCHA_SECRET_KEY")
# VERIFY_URL = getattr(settings, "VERIFY_URL", "https://hcaptcha.com/siteverify")


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = "accounts/snippets/captcha.html"


class ReactivationEmailForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                # "placeholder": "Email",
                "class": "mx-auto flex border border-gray-300 hover:border-gray-500 py-1 px-2 my-3 rounded-lg shadow placeholder-gray-600 focus:outline-none",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_disposable_email(email)
        except ValidationError:
            pass
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("register")
            msg = f'New email, would you like to <a href="{register_link}">sign up</a>?'
            raise forms.ValidationError(mark_safe(msg))
        return email


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                # "placeholder": "",
                "class": "border border-gray-500 py-1 px-1 rounded-lg shadow placeholder-gray-800",
                "autocomplete": "current-password",
                "autofocus": True,
            }
        ),
    )
    # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)# remove friction

    class Meta:
        model = USER
        fields = ("email", "password")  # 'first_name'

    # def clean_password2(self):
    #     # Check whether the two password match
    #     password = self.cleaned_data.get("password")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        # Save password in hash format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.active = True
        if commit:
            user.save()
        return user


class UserDetailChangeForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("First name"),
        required=False,
        widget=forms.TextInput(
            attrs={
                # "placeholder": _("First name"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=False,
        widget=forms.TextInput(
            attrs={
                # "placeholder": _("Last name"),
                "class": "w-full flex border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )

    class Meta:
        model = USER
        fields = ("first_name", "last_name")


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = USER
        fields = (
            "email",
            "password",
            "first_name",
            "is_active",
            "is_staff",
        )

    def clean_password(self):
        return self.initial["password"]


# birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'})) pikaday


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "id": "id_email",
                # "placeholder": "Email",
                "autofocus": True,
                "class": "w-full border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_password",
                # "placeholder": _("Password"),
                "autocomplete": "current-password",
                "class": "w-full border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )  # 'data-toggle': 'password,'
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
    # Removed to smooth UX
    # password2 = forms.CharField(label='', strip=False, widget=forms.PasswordInput(
    #     attrs={'placeholder': 'Confirm Password'

    # captcha = ReCaptchaField(label='', widget=ReCaptchaV3)
    # captcha = ReCaptchaField(label='', widget=ReCaptchaV2Checkbox(
    #     attrs={
    #         'data-theme': 'dark',
    #         'data-size': 'compact',
    #     }#, api_params={'hl': 'cl', 'onload': 'onLoadFunc'}
    #     )#, public_key='76wtgdfsjhsydt7r5FFGFhgsdfytd656sad75fgh',
    # #private_key='98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs',
    # )

    # password = PasswordField()# add psw strength estimator on the frontend js
    # password2 = PasswordConfirmationField(confirm_with='password1')
    class Meta:
        model = USER
        fields = ("email", "password")  # 'password2'(RegistrationForm.Meta)

    def save(self, commit=True):
        # Save the password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()  # [Errno 101] Network is unreachable
        return user

    # def __init__(self, *args, **kwargs):
    #     super(RegisterForm, self).__init__(*args, **kwargs)
    #     self. helper .layout = Layout(
    #             Div(data_sitekey=HCAPTCHA_SECRET_KEY, css_class='h-captcha')
    #         )

    # def clean_password2(self):
    #     """Check whether the two psw entries match"""
    #     password = self.cleaned_data.get("password")
    #     password2 = self.cleaned_data.get("password2")
    # #     if password2:
    # #         score = zxcvbn(password1)['score']# score is between 0 and 4
    #     if password and password2 and password != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "id": "id_email",
                # "placeholder": "Email",
                "class": "w-full border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "id": "id_password",
                # "placeholder": _("Password"),
                "class": "w-full border border-gray-300 focus:border-yellow-500 py-1 px-2 rounded-lg shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
                "autocomplete": "current-password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )  # 'data-toggle': 'password'
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
    # ReCaptchaField(label='', widget=ReCaptchaV3)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        try:
            validate_disposable_email(email)
        except:
            raise ValidationError(
                self.error_messages["invalid_login"], code="invalid_login"
            )
        #     raise ValidationError(
        #         self.error_messages['password_mismatch'],
        #         code='password_mismatch',
        #     )
        # password_validation.validate_password(password2, self.user)
        password = data.get("password")
        qs = USER.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                # not active, check email activation
                link = reverse("account:resend-activation")
                reconfirm_ms = f'<a href="{link}">Resend confirmation email</a>.'
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    _ms = (
                        _("Please check your email to confirm your account or ")
                        + reconfirm_ms.lower()
                    )
                    raise forms.ValidationError(mark_safe(_ms))
                email_confirm_exists = EmailActivation.objects.email_exists(
                    email
                ).exists()
                if email_confirm_exists:
                    msg2 = _("Email not confirmed. ") + reconfirm_ms
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError(_("This email is inactive"))
        user = authenticate(request, email=email, password=password)
        if user is None:
            raise forms.ValidationError(_("Invalid credentials"))
        login(request, user)
        self.user = user
        USER_LOGGED_IN.send(user.__class__, instance=user, request=request)
        # try:
        #     del request.session['guest_email_id']
        # except:# handle specific exception as _e:
        #     # print(f'Error {_e.message} occured. Arguments {_e.args}')
        #     pass
        return data


# class AuthenticationForm(forms.Form):
#     """
#     Base class for authenticating users. Extend this to get a form that accepts
#     username/password logins.
#     """

#     username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
#     password = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
#     )

#     error_messages = {
#         "invalid_login": _(
#             "Please enter a correct %(username)s and password. Note that both "
#             "fields may be case-sensitive."
#         ),
#         "inactive": _("This account is inactive."),
#     }

#     def __init__(self, request=None, *args, **kwargs):
#         """
#         The 'request' parameter is set for custom auth use by subclasses.
#         The form data comes in via the standard 'data' kwarg.
#         """
#         self.request = request
#         self.user_cache = None
#         super().__init__(*args, **kwargs)

#         # Set the max length and label for the "username" field.
#         self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
#         username_max_length = self.username_field.max_length or 254
#         self.fields["username"].max_length = username_max_length
#         self.fields["username"].widget.attrs["maxlength"] = username_max_length
#         if self.fields["username"].label is None:
#             self.fields["username"].label = capfirst(self.username_field.verbose_name)

#     def clean(self):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")

#         if username is not None and password:
#             self.user_cache = authenticate(
#                 self.request, username=username, password=password
#             )
#             if self.user_cache is None:
#                 raise self.get_invalid_login_error()
#             else:
#                 self.confirm_login_allowed(self.user_cache)

#         return self.cleaned_data

#     def confirm_login_allowed(self, user):
#         """
#         Controls whether the given User may log in. This is a policy setting,
#         independent of end-user authentication. This default behavior is to
#         allow login by active users, and reject login by inactive users.
#         If the given user cannot log in, this method should raise a
#         ``ValidationError``.
#         If the given user may log in, this method should return None.
#         """
#         if not user.is_active:
#             raise ValidationError(
#                 self.error_messages["inactive"],
#                 code="inactive",
#             )

#     def get_user(self):
#         return self.user_cache

#     def get_invalid_login_error(self):
#         return ValidationError(
#             self.error_messages["invalid_login"],
#             code="invalid_login",
#             params={"username": self.username_field.verbose_name},
#         )


# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from settings.utils import account_activation_token
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage

# current_site = get_current_site(request)
# mail_subject = 'Activate your account.'
# message = render_to_string('acc_active_email.html', {
#     'user': user,
#     'domain': current_site.domain,
#     'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
#     'token':account_activation_token.make_token(user),
# })
# to_email = form.cleaned_data.get('email')
# email = EmailMessage(
#             mail_subject, message, to=[to_email]
# )
# email.send()
# return HttpResponse('Please confirm your email address to complete the registration')
