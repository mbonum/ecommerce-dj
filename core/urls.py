# import debug_toolbar
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from django.contrib.sitemaps.views import sitemap
from django.urls import include, path  # , re_path
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from django.views.decorators.csrf import csrf_exempt

# # from filebrowser.sites import site
# from graphene_django.views import GraphQLView

# from .schema import schema $ graphene
from accounts.views import LoginView, RegisterView
from core.views import robots_txt
from essays.sitemaps import EssaySitemap

# from essays.admin import essays_admin # add separate CMS for authors

from marketing.views import MailchimpWebhookView, MarketingPreferenceUpdateView
from orders.views import GenerateOrderPDF, LibraryView

# # from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls
# # from two_factor.urls import urlpatterns as tf_urls


sitemaps = {
    "essays": EssaySitemap,  # static
}

urlpatterns = [
    # https://pypi.org/project/drfpasswordless/
    path("", include("drfpasswordless.urls")),
    path("", include("home.urls", namespace="home")),
    path("captcha/", include("captcha.urls")),
    path(_("contact/"), include("chat.urls", namespace="chat")),  # channels
    # separate CMS only authors can access , schema=schema graphene
    # path(_('write/bmltZGEtbWdiLTI1Cg'), essays_admin.urls),
    path(_("read/"), include("essays.urls", namespace="read")),# path("hitcount/", include("hitcount.urls", namespace="hitcount")),
    path(_("learn/"), include("education.urls", namespace="learn")),
    path(_("team/"), include("team.urls", namespace="team")),
    path(_("shop/"), include("shop.urls", namespace="shop")),
    path(_("search/"), include("search.urls", namespace="search")),
    path(_("cart/"), include("carts.urls", namespace="cart")),
    path(_("signup/"), RegisterView.as_view(), name="register"),
    path(_("login/"), LoginView.as_view(), name="login"),
    path(_("logout/"), LogoutView.as_view(), name="logout"),
    path(_("address/"), RedirectView.as_view(url="/addresses")),
    path(_("addresses/"), include("addresses.urls", namespace="address")),
    path(_("billing/"), include("billing.urls", namespace="billing")),
    path(_("orders/"), include("orders.urls", namespace="orders")),
    path(_("invoice/<slug:_id>/"), GenerateOrderPDF.as_view(), name="invoice"),
    path(_("library/"), LibraryView.as_view(), name="library"),
    path(_("settings/"), RedirectView.as_view(url="/account")),
    path(_("accounts/"), RedirectView.as_view(url="/account")),
    path(_("account/"), include("accounts.urls", namespace="account")),
    path(_("accounts/"), include("accounts.passwords.urls")),  # templates/registration
    path(_("analytics/"), include("analytics.urls", namespace="analytics")),
    path(_("newsletter/"), include("newsletter.urls")),  # , namespace='newsletter'
    path(_("settings/email/"), MarketingPreferenceUpdateView.as_view(), name="email-marketing-pref",),
    path("webhooks/mailchimp/", MailchimpWebhookView.as_view(), name="webhooks-mailchimp"),
    path("clvm/", include("shorturl.urls", namespace="clvm")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", robots_txt),  # or create template/robots.txt
    # TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots-txt",
    # # DL model
    # # path('classify/', views.call_model.as_view()),
    # # path('note/', include('todolists.api.urls', namespace='note')),
    # # path('ebook/', include('ebooks.api.urls', namespace='ebook')),
    # # path('profile/', include('profiles.api.urls', namespace='profile')),
    # path("tinymce/", include("tinymce.urls")),
    # # path('c2l0ZW1hcHMudHh/', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views'),
    # # 64encode sitemaps.txt robot.xml
    # path('cm9ib3QueG1s0/', include('robots.urls')),
    # # path('InRyYWNrLWluZyJcbm90TUU=/', include('tracking.urls')),# tracking2 "track-ing"\notME
    # # path("bmltZGEtbWdiLTI1Cg/defender/", include("defender.urls")),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
]

# urlpatterns += i18n_patterns()

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns.append(path("rosetta/", include("rosetta.urls")))

try:
    urlpatterns.append(
        path("bmltZGEtbWdiLTI1Cg/", include(admin.site.urls, namespace="admin"))
    )
except:
    urlpatterns.append(path("bmltZGEtbWdiLTI1Cg/", admin.site.urls, name="admin"))

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # from django.views.static import serve
    # if settings.DEBUG:
    #     urlpatterns += [
    #         re_path(r'^media/(?P<path>.*)$', serve, {
    #             'document_root': settings.MEDIA_ROOT,
    #         }),
    #     ]
    # urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    # urlpatterns += (
    #     path(
    #         "graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))
    #     ),
    # )


admin.site.site_header = getattr(settings, "ENV_NAME", "Clavem") + " admin"
admin.site.index_title = "Home"
admin.site.site_title = admin.site.site_header
