# from django.utils.http import is_safe_url from django_registration.forms import RegistrationForm
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV3#, ReCaptchaV2Checkbox
from django import forms
from django.conf import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
)  # , password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe
from captcha.fields import CaptchaField, CaptchaTextInput
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
        label="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "m-auto flex border border-gray-300 hover:border-gray-500 py-1 px-2 my-3 rounded shadow placeholder-gray-600",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
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
                "placeholder": "",
                "class": "border border-gray-500 py-1 px-1 rounded shadow placeholder-gray-800",
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
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "m-auto flex border border-gray-300 hover:border-gray-500 py-1 px-2 rounded shadow placeholder-gray-600",
            }
        ),
    )
    last_name = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "m-auto flex border border-gray-300 hover:border-gray-500 py-1 px-2 mt-3 rounded shadow placeholder-gray-600",
            }
        ),
    )
    # full_name = forms.CharField(label='Name', required=False,
    # widget=forms.TextInput(attrs={'class':'form-control'}))

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
            "is_active",# remove
            "is_staff",
        )

    def clean_password(self):
        return self.initial["password"]


# birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'})) pikaday


class RegisterForm(forms.ModelForm):

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "w-full flex border border-gray-300 py-1 px-2 rounded shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-100 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "w-full flex border border-gray-300 py-1 px-2 my-3 rounded shadow placeholder-gray-600 focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )  # 'data-toggle': 'password,' strip=False
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
    # help_text=password_validation.password_validators_help_text_html()
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
        fields = (
            "email",
            "password",
        )  # 'full_name', 'password2'(RegistrationForm.Meta)

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
        label=" ",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "w-full flex border border-gray-300 py-1 px-2 rounded shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
            }
        ),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "w-full flex border border-gray-300 py-1 px-2 rounded shadow placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-200 focus:ring-offset-transparent focus:ring-offset-2",
                "autocomplete": "current-password",
                "autofocus": True,
            }
        ),
    )  # 'autocomplete': 'off', 'data-toggle': 'password'
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
    # captcha = ReCaptchaField(label='', widget=ReCaptchaV3)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
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
                    msg2 = "Email not confirmed. " + reconfirm_ms
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


# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from settings.utils import account_activation_token
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage

# current_site = get_current_site(request)
# mail_subject = 'Activate your blog account.'
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
