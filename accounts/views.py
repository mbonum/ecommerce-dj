# import json
# import requests
# from django.http import Http404, HttpResponse
from core.mixins import NextUrlMixin, RequestFormAttachMixin

# from core.utils import account_activation_token
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# from django.contrib.auth import authenticate, login#, get_user_model
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage, send_mail
from django.shortcuts import redirect, render

# from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

# from django.utils.encoding import force_bytes, force_text
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, FormView, UpdateView, View
from django.views.generic.edit import FormMixin

from .forms import LoginForm, ReactivationEmailForm, RegisterForm, UserDetailUpdateForm
from .models import CUser, EmailActivation

# RECAPTCHAV3_SECRET = getattr('RECAPTCHAV3_SECRET')
# CAPTCHA_SECRET = getattr('CAPTCHA_SECRET')VERIFY_URL = settings('VERIFY_URL', 'https://hcaptcha.com/siteverify')


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = "accounts/user-home.html"
    key = None

    def get_object(self):
        return self.request.user

    def form_invalid(self, form):
        key = self.key
        context = {"form": form, "key": key}
        return render(self.request, "registration-error.html", context)


class AccountEmailActivateView(FormMixin, View):
    # Send email when user creates an account SuccessMessageMixin
    success_url = reverse_lazy("login")
    form_class = ReactivationEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(
                    request, _("Your email has been confirmed. Please login.")
                )
                return redirect("login")
            activated_qs = qs.filter(activated=True)
            if activated_qs.exists():
                reset_link = reverse("password_reset")
                msg = (
                    _("Your account has been activated. Do you need to")
                    + f'<a href="{reset_link}">'
                    + _("update your password?")
                    + "</a>"
                )  # Your email has already been confirmed
                messages.info(request, mark_safe(msg))
                return redirect("login")
        context = {"form": self.get_form(), "key": key}
        return render(request, "registration/activation-error.html", context)

    def post(self):
        # Create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(
            self.request, _("Activation link sent, please check your email.")
        )
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        usr = obj.user
        new_activation = EmailActivation.objects.create(user=usr, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {"form": form, "key": self.key}
        return render(self.request, "registration/activation-error.html", context)

# from .forms import UserUpdateForm,ProfileUpdateForm
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
#         u_form = UserUpdateForm(request.POST,instance=request.user)
#         if p_form.is_valid() and u_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request,'Your Profile has been updated!')
#             return redirect('profile')
#     else:
#         p_form = ProfileUpdateForm(instance=request.user)
#         u_form = UserUpdateForm(instance=request.user.profile)

#     context={'p_form': p_form, 'u_form': u_form}
#     return render(request, 'users/profile.html',context )


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/edit-profile.html"
    form_class = UserDetailUpdateForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context["title"] = _("Edit Profile")  # Personilize Account Details
        context["img"] =  self.request.user.img
        if self.request.user.first_name:
            context["fn"] = self.request.user.first_name
        else:
            context["usr"] = self.request.user.get_usrname
        return context

    def form_valid(self, form):
        messages.success(
            self.request, _("Account Updated")
        )
        img = self.request.FILES
        # form.cleaned_data.get("img")
        first_name = form.cleaned_data.get("first_name")
        # None
        last_name = form.cleaned_data.get("last_name")
        usr = CUser.objects.get(email=self.request.user)
        usr.img = img
        usr.first_name = first_name
        usr.last_name = last_name
        return super(UserDetailUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("account:user-update")


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):  # SuccessMessageMixin
    form_class = LoginForm
    template_name = "accounts/login.html"
    # success_url = "/" # reverse_lazy("home")
    # success_message = _("Welcome back")

    def form_valid(self, form):
        human = True
        return redirect(self.get_next_url())


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    # send email link to confirm automatic block if it's not confirmed within 48 hours
    success_url = reverse_lazy("login")
    success_message = _(
        "Check your email and click on the link to activate your account."
    )

    def form_valid(self, form):
        human = True
        return redirect("login")

    # def form_invalid(self, form, **kwargs):
    # invalid if email is temp -> compare domain with temp-email.txt

    # def get_success_url(self):
    #     return self.get_next_url()
    # request = self.request
    # msg = "Thank you to sign up."
    # messages.success(request, msg)
    # subject = 'Activate your' + C + ' account'
    # msg = 'Please confirm your account clicking on the link below. Thanks'
    # from_email = settings.EMAIL_HOST_USER
    # to_list = form_class.cleaned_data.get('email')
    # send_mail(subject, msg, from_email, to_list, fail_silently=True)

    # if form.is_valid():
    ## hCaptcha validation
    # token = requests.POST.get['h-captcha-response']

    ## Build payload with secret key and token.
    # data = { 'secret': settings.HCAPTCHA_SECRET_KEY, 'response': token }

    ## Make POST request with data payload to hCaptcha API endpoint.
    # response = requests.post(url=settings.VERIFY_URL, data=data)

    ## Parse JSON from response. Check for success or error codes.
    # response_json = json.parse(response.content)
    # success = response_json['success']
    # your_captcha_response = requests.POST.get('h-captcha-response')
    # data = {
    #     'secret': settings.HCAPTCHA_SECRET_KEY,
    #     'response': your_captcha_response
    # }
    # r = requests.post(settings.VERIFY_URL, data=data)
    # result = r.json()
    # if result['success']:
    #     """Clean the form, save, and send email."""
    #     # Your cleaning form code.
    #     # Your save the form code
    #     your_form = form.save(commit=False)
    #     # Send the email. AccountEmailActivateView
    #     try:
    #         # Your sending email code
    #         pass
    #     except BadHeaderError:
    #         return HttpResponse('Invalid header found.')
    #     # Save the form.
    #     your_form.save()
    #     # Redirect to a new url.
    #     return redirect('your/redirect/url')
    # else:
    # context = {
    #     'form': YourCrispyForm,
    #     'invalid_hcaptcha': messages.add_message(request, messages.INFO, 'Your message.')
    # }

    # def send_activation(self):
    #     current_site = get_current_site(self)#request
    #     mail_subject = 'Activate your Armonia account'
    #     message = render_to_string('email_activation.html', {
    #         'user': form_class.cleaned_data.get('email'),
    #         'domain': current_site.domain,
    #         'uid': urlsafe_base64_encode(force_bytes(USER.pk)).decode(),
    #         'token': account_activation_token.make_token(USER),
    #     })
    #     to_email = form_class.cleaned_data.get('email')
    #     email = EmailMessage(mail_subject, message, to=[to_email])
    #     email.send()
    #     return HttpResponse('Please confirm your email address to complete the registration')

    #     if request.method == 'POST':
    #     form = SignupForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.is_active = False
    #         user.save()
    #         current_site = get_current_site(request)
    #         mail_subject = 'Activate your blog account.'
    #         message = render_to_string('acc_active_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
    #             'token':account_activation_token.make_token(user),
    #         })
    #         to_email = form.cleaned_data.get('email')
    #         email = EmailMessage(
    #                     mail_subject, message, to=[to_email]
    #         )
    #         email.send()
    #         return HttpResponse('Please confirm your email address to complete the registration')
    # else:
    #     form = SignupForm
    # return render(request, 'signup.html', {'form': form})

    # def activate(request, uidb64, token):
    #     try:
    #         uid = force_text(urlsafe_base64_decode(uidb64))
    #         user = User.objects.get(pk=uid)
    #     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    #         user = None
    #     if user is not None and account_activation_token.check_token(user, token):
    #         user.is_active = True
    #         user.save()
    #         login(request, user)
    #         # return redirect('home')
    #         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    #     else:
    #         return HttpResponse('Activation link is invalid!')

    # request.GET.get('next')
    #     next_post = request.POST.get('next')
    #     redirect_path = next_ or next_post or None


# from django.http import response import http
# from allauth_2fa.middleware import BaseRequire2FAMiddleware # https://django-allauth-2fa.readthedocs.io/en/latest/advanced/

# class RequireSuperuser2FAMiddleware(BaseRequire2FAMiddleware):
#     """Force User to use 2FA"""
#     def require_2fa(self, request):
#         # Superusers are require to have 2FA.
#         return request.user.is_superuser

# from .signals import user_logged_in

# def captcha(request):
#     """https://dashboard.hcaptcha.com/welcome CAPTCHA validation"""
#     # params = {
#     #     'secret': "SECRET_KEY",
#     #     'response': token
#     # }
#     # json = http.POST('VERIFY_URL', params)

#     # Retrieve token from post data with key 'h-captcha-response'.
#     # token = request.POST["h-captcha-response"]
#     token = request.POST_DATA['h-captcha-response']

#     # Build payload with secret key and token.
#     data = {'secret': SECRET_KEY, 'response': token}

#     # Make POST request with data payload to hCaptcha API endpoint.
#     response = http.POST(url=VERIFY_URL, data=data)

#     # Parse JSON from response. Check for success or error codes.
#     response_json = json.parse(response.content)
#     success = response_json['success']

# Implementing function-based view using the decorator login_required
# @login_required # force to go to /accounts/login/?next=/somepath/
# def account_home_view(request):
#     return render(request, 'accounts/home.html', {})

# alternative
# class LoginRequiredMixin(object):
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(self, request, *args, **kwargs)
# But django.contrib.auth.mixins has already LoginRequiredMixin

# def login(request):
#     """Simple Login"""
#     form = LoginForm(request.POST or None)
#     context = {'form': form}
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('/')

# class GuestRegisterView(NextUrlMixin, RequestFormAttachMixin, CreateView):
#     form_class = GuestForm
#     default_next = '/register/'

#     def get_success_url(self):
#         request = self.request
#         msg = "Thank you to be our guest. You're welcome to sign up."
#         messages.success(request, msg)
#         return self.get_next_url()

#     def form_invalid(self, form):
#         return redirect(self.default_next)

# passwordless
# import base64
# import logging
# import random
# import string
# import time

# import jwt# pip install jwt


# class Pypale:
#     JWT_ALGORITHM = 'HS256'
#     ENCODING = 'utf8'

#     def __init__(self, token_ttl_minutes: int, base_url: str, secret_key: str,
#                  token_issue_ttl_seconds: int):
#         self.token_ttl_minutes = token_ttl_minutes
#         self.base_url = base_url
#         self.secret_key = secret_key
#         self.token_issue_ttl_seconds = token_issue_ttl_seconds

#     def generate_token(self, email: str):#) -> str
#         return base64.b64encode(
#             jwt.encode(self.generate_token_metadata(email), self.secret_key,
#                        algorithm=self.JWT_ALGORITHM)).decode(self.ENCODING)

#     def generate_token_metadata(self, email: str) -> dict:
#         return {
#             'sub': email,
#             'jti': self.one_time_nonce(),
#             'iat': int(time.time()),
#             'exp': int(time.time()) + (self.token_ttl_minutes * 60),
#             'iss': self.base_url
#         }

#     def one_time_nonce(
#         self,
#         size=16,
#         chars=string.ascii_letters + string.digits + '-') -> str:
#         return ''.join(random.choice(chars) for _ in range(size))

#     def valid_token(self, return_token: str, return_email: str = '') -> bool:
#         try:
#             decoded_return_token = base64.b64decode(return_token).decode(
#                 self.ENCODING)
#             token_metadata = jwt.decode(decoded_return_token,
#                                         self.secret_key,
#                                         algorithms=[self.JWT_ALGORITHM])
#             if (token_metadata['iat'] + self.token_issue_ttl_seconds) < int(
#                     time.time()):
#                 logging.warning('Token was issued too long ago.')
#                 return False
#             elif return_email != '':
#                 if token_metadata['sub'] != return_email:
#                     logging.warning('Token is not issued to the right user.')
#                     return False
#                 return True
#             else:
#                 return True
#         except Exception as e:
#             logging.exception(
#                 f'Raised exception while validating login link: {e}')
#             return False

# from pypale import Pypale
# class Pswless(View):
#     token_ttl_minutes = 14 * 24 * 60 # 2 weeks
#     token_issue_ttl_seconds = 2 * 60 * 60 # 2 hours
#     base_url = 'clavem.co'
#     secret_key = settings('SECRET_KEY')

#     pypale = Pypale(
#         base_url=base_url,
#         secret_key=secret_key,
#         token_ttl_minutes=token_ttl_minutes,
#         token_issue_ttl_seconds=token_issue_ttl_seconds)

#     email = 'mr.m.bonomi@gmail.com'
#     token = pypale.generate_token(email)
#     assert pypale.valid_token(token, email)