# import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView

# from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from django.views.decorators.csrf import csrf_exempt

# # from filebrowser.sites import site
# from graphene_django.views import GraphQLView

# from .schema import schema
from accounts.views import LoginView, RegisterView
from carts.views import cart_detail_api_view

# # from essays.sitemaps import EssaySitemap
from essays.views import GenerateEssayPDF, author_view
# # from essays.admin import essays_admin

# from marketing import urls as mktg_urls
# from marketing.views import MailchimpWebhookView, MarketingPreferenceUpdateView
from orders.views import GenerateOrderPDF, LibraryView
from shorturl.views import ShortURLView, URLRedirectView
# # from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls
# # from two_factor.urls import urlpatterns as tf_urls


# vue
# router = routers.DefaultRouter()
# router.register(r'notes', NotesViewSet)
# path('', include(router.urls)),

# SITEMAPS = {
#     'static': EssaySitemap,
# }

urlpatterns = [
    # path(
    #     "robots.txt",
    #     TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    #     name="robots-txt",
    # ),
    path("captcha/", include("captcha.urls")),
    path(
        "", include("drfpasswordless.urls")
    ),  # https://pypi.org/project/drfpasswordless/
    path("", include("home.urls", namespace="home")),
    path(_("chat/"), include("chat.urls")),
    # # create a separate CMS that only authors can access, schema=schema
    # # path(_('essays/'), essays_admin.urls),
    path(_("read/"), include("essays.urls", namespace="read")),
    # #     path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path(_("author/<slug:slug>/"), author_view, name="author"),
    path("pdf/<slug:slug>/", GenerateEssayPDF.as_view(), name="pdf"),
    path(_("learn/"), include("education.urls", namespace="learn")),
    # # path('edu-pdf/<slug:slug>/', GenerateEduPDF.as_view(), name='edu-pdf'),
    path(_("team/"), include("team.urls", namespace="team")),
    path(_("shop/"), include("products.urls", namespace="products")),
    path(_("search/"), include("search.urls", namespace="search")),
    path(_("cart/"), include("carts.urls", namespace="cart")),
    path("api/cart/", cart_detail_api_view, name="api-cart"),  # YXBpL2NhcnQv/
    path(_("signup/"), RegisterView.as_view(), name="register"),
    path(_("login/"), LoginView.as_view(), name="login"),
    path(_("logout/"), LogoutView.as_view(), name="logout"),
    path(_("address/"), RedirectView.as_view(url="/addresses")),
    path(_("addresses/"), include("addresses.urls", namespace="address")),
    path(_("billing/"), include("billing.urls", namespace="billing")),
    # path(_("billing/payment-method/"), payment_method_view, name="billing-payment-method"),
    # path(_("billing/payment-method/create/"), payment_method_createview, name="billing-payment-method-end"),
    path(_("orders/"), include("orders.urls", namespace="orders")),
    path(_("invoice/<slug:_id>/"), GenerateOrderPDF.as_view(), name="order-pdf"),
    path(_("library/"), LibraryView.as_view(), name="library"),
    path(_("settings/"), RedirectView.as_view(url="/account")),
    path(_("accounts/"), RedirectView.as_view(url="/account")),
    path(_("account/"), include("accounts.urls", namespace="account")),
    path(_("accounts/"), include("accounts.passwords.urls")),  # templates/registration
    path(_("analytics/"), include("analytics.urls", namespace="analytics")),
    # #     path(_('newsletter/'), include('newsletter.urls')), #, namespace='newsletter'
    # #     # path('', Subscribe.as_view(), name='subscribe'),
    # #     # path('subscribe-api/', include(mktg_urls)),
    # #     path(_('settings/email/'), MarketingPreferenceUpdateView.as_view(),
    # #          name='marketing-pref'),
    # #     path('webhooks/mailchimp/', MailchimpWebhookView.as_view(),
    # #          name='webhooks-mailchimp'),
    # #     # DL model
    # #     # path('classify/', views.call_model.as_view()),
    # #     # path('note/', include('todolists.api.urls', namespace='note')),
    # #     # path('ebook/', include('ebooks.api.urls', namespace='ebook')),
    # #     # path('profile/', include('profiles.api.urls', namespace='profile')),
    # path("tinymce/", include("tinymce.urls")),
    # #     # path('c2l0ZW1hcHMudHh/', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views'),
    # #     # 64encode sitemaps.txt robot.xml
    # #     path('cm9ib3QueG1s0/', include('robots.urls')),
    # #     # path('InRyYWNrLWluZyJcbm90TUU=/', include('tracking.urls')),# tracking2 "track-ing"\notME
    # path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    # # path("bmltZGEtbWdiLTI1Cg/defender/", include("defender.urls")),
    # # short urls
    # re_path(r"^c/(?P<shortcode>[\w-]+)/$", URLRedirectView.as_view(), name="clvmcode"),
    # path("c/", ShortURLView.as_view(), name="clvmurl") # only for admin
]

# urlpatterns += i18n_patterns()

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns.append(path("rosetta/", include("rosetta.urls")))  # += []

try:
    urlpatterns.append(path("bmltZGEtbWdiLTI1Cg/", include(admin.site.urls)))
except:
    urlpatterns.append(path("bmltZGEtbWdiLTI1Cg/", admin.site.urls))

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    # urlpatterns += (
    #     path(
    #         "graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))
    #     ),
    # )
    # path('s/', include('shortener.urls')),


admin.site.site_header = getattr(settings, "ENV_NAME", "Clavem") + " admin"
admin.site.index_title = ""
admin.site.site_title = admin.site.site_header

# re_path(r'^', include('allauth_2fa.urls')),
# re_path(r'^', include('allauth.urls')),
# path('otpadmin/', admin_site.urls),
# path('read/', include('django.contrib.flatpages.urls')),
# path('', include(tf_urls)),
# path('', include(tf_twilio_urls)),
# path('', TemplateView.as_view(template_name='index.html'), name='index'), # vue
# re_path(r'^.*$', IndexTemplateView.as_view(), name='entry-point'),
# path('bmltZGEtbWdiLTI1Cg/filebrowser/', site.urls),
# path('grappelli/', include('grappelli.urls')),
# path('.well-known/', include('letsencrypt.urls')),
# path('', include('pwa.urls')),
# path('xicon/', include('xicon.urls')),
# https://base64encode.org nimda-mgb-25
# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]


# from dl import views
# from subscribe.views import Subscribe
# from core.views import IndexTemplateView
# from rest_auth.views import LoginView

# https://django-registration.readthedocs.io/en/3.1/activation-workflow.html
# from django_registration.backends.one_step.views import RegistrationView# two_step

# from two_factor.admin import AdminSiteOTPRequired, AdminSiteOTPRequiredMixin


# class AdminSiteOTPRequiredMixinRedirSetup(AdminSiteOTPRequired):
#     def login(self, request, extra_context=None):
#         redirect_to = request.POST.get(
#             REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME)
#         )
#         # For users not yet verified the AdminSiteOTPRequired.has_permission
#         # will fail. So use the standard admin has_permission check:
#         # (is_active and is_staff) and then check for verification.
#         # Go to index if they pass, otherwise make them setup OTP device.
#         if request.method == 'GET' and super(
#             AdminSiteOTPRequiredMixin, self
#         ).has_permission(request):
#             # Already logged-in and verified by OTP
#             if request.user.is_verified():
#                 # User has permission
#                 index_path = reverse('admin:index', current_app=self.name)
#             else:
#                 # User has permission but no OTP set:
#                 index_path = reverse('two_factor:setup', current_app=self.name)
#             return HttpResponseRedirect(index_path)

#         if not redirect_to or not is_safe_url(
#             url=redirect_to, allowed_hosts=[request.get_host()]
#         ):
#             redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
#         return redirect_to_login(redirect_to)


# Enforce two factor authentication in the admin and use the default admin site
# admin.site.__class__ = AdminSiteOTPRequired

# admin_site = OTPAdmin(name='OTPAdmin')

# from django_otp.admin import OTPAdminSite
# class OTPAdmin(OTPAdminSite):
#     pass
# from django_otp.plugins.otp_totp.models import TOTPDevice
# admin_site = OTPAdmin(name='OTPAdmin')
# admin_site.register(User)
# admin_site.register(TOTPDevice)
