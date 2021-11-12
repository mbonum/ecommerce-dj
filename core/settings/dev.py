from .base import *

DEBUG = config("DEBUG", default=False, cast=bool)

try:
    SECRET_KEY = config("SECRET_KEY")
except KeyError:
    raise ImproperlyConfigured("SECRET_KEY environment variable is missing!")

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")

# ALLOWED_HOSTS += [
#     'subdomain.localhost',# add subdomains in hosts.py and on porkbun
# ]

# /home/mgb/.local/share/virtualenvs/a1-dVYVCYMC/lib/python3.9/site-packages/newsletter/ model
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    # "django.core.mail.backends.filebased.EmailBackend"
    # EMAIL_FILE_PATH = BASE_DIR / "emails"
else:
    EMAIL_BACKEND = config(
        "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
    )

EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")  # protonmail
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="support@clavem.co")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)  # 1025
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
# EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=True, cast=bool)
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # (,) #support@clavem.co ENV_NAME + ' <support@' + BASE_URL + '>'# Customer Care


INSTALLED_APPS += [
    "home",
    # "chat",
    "accounts",
    "essays",
    "notes",
    "education",
    "team",
    "marketing",
    "shop",
    "search",
    "tags",
    "carts",
    "addresses",
    "billing",
    "orders",
    "analytics",
    "shorturl",
    "ariadne.contrib.django",# "graphene_django",
]

AUTH_USER_MODEL = "accounts.CUser"

SESSION_COOKIE_CART = 86400
CART_SESSION_ID = "cart"

# GRAPHENE = {"SCHEMA": "core.schema.schema"}

# https://docs.djangoproject.com/en/3.1/topics/logging/
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '.log/debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'filters': {
#         # 'special': {
#         #     '()': 'project.logging.SpecialFilter',
#         #     'foo': 'bar',
#         # },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '.log/debug.log',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             # 'filters': ['special']
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file'],
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         # 'core.custom': {
#         #     'handlers': ['console', 'mail_admins'],
#         #     'level': 'INFO',
#         #     'filters': ['special']
#         # }
#     }
# }

CORS_ORIGIN_ALLOW_ALL = False
CORS_REPLACE_HTTPS_REFERER = False
CSP_DEFAULT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://polyfill.io/",
    "https://commerce.coinbase.com/",
    "https://js.stripe.com/",
    "https://checkout.stripe.com",
)  # "https://www.google.com/recaptcha/", "https://www.gstatic.com/recaptcha/", "https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.5.0/dist/alpine.min.js"  "'nonce-lrEwC5VX0M'" "https://chimpstatic.com/mcjs-connected/js/users/0e61ec17658f41b70da7d62f5/0a42a86cd2c1b1c3c4bc6025d.js", "https://hcaptcha.com", "https://*.hcaptcha.com", "https://chimpstatic.com/mcjs-connected/js/users/0e61ec17658f41b70da7d62f5/0a42a86cd2c1b1c3c4bc6025d.js", "https://polyfill.io/v3/polyfill.min.js", "https://cdnjs.cloudflare.com/ajax/libs/jsrender/1.0.6/jsrender.js", "https://cdn.jsdelivr.net/npm/marked/marked.min.js", "https://cdn.jsdelivr.net/npm/darkmode-js@1.5.6/lib/darkmode-js.min.js",
CSP_FRAME_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://polyfill.io/v3/polyfill.min.js",
    "https://commerce.coinbase.com/",
    "https://js.stripe.com",
    "https://hooks.stripe.com",
    "https://checkout.stripe.com",
)  # "https://www.google.com/recaptcha/", "https://hcaptcha.com", "https://*.hcaptcha.com", , "https://cdn.jsdelivr.net/npm/darkmode-js@1.5.6/lib/darkmode-js.min.js",
CSP_CONNECT_SRC = ("'self'", "https://api.stripe.com", "https://checkout.stripe.com")
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
)  # , "https://hcaptcha.com", "https://*.hcaptcha.com", "https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.css", "https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.css",
CSP_FONT_SRC = ("'self'",)
CSP_IMG_SRC = (
    "'self'",
    "https://*.stripe.com",
)  # "'strict-dynamic'", "'https://www.paypal.com/en_IT/i/scr/pixel.gif'",
CSP_MEDIA_SRC = (
    "'self'",
    "https://polyfill.io/v3/polyfill.min.js",
    "https://commerce.coinbase.com/",
    "https://js.stripe.com/",
)

HOST_SCHEME = "http://"  # https://
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False
SECURE_HSTS_PRELOAD = False

# smtp.gmail.com https://support.google.com/mail/answer/7126229?visit_id=637475480606318471-1042357849&rd=2#cantsignin
# Requires SSL: Yes
# Requires TLS: Yes (if available)
# Requires Authentication: Yes
# Port for SSL: 465
# Port for TLS/STARTTLS: 587

# CELERY_BROKER_URL = "amqp://localhost"  # URI from Heroku redis app
# # CELERY_TIMEZONE = "Australia/Tasmania"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'

SHORTCODE_MAX = 7
SHORTCODE_MIN = 5
