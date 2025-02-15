# import os
import sys
from pathlib import Path

# , Csv # pip install python-decouple
# import django_heroku
import dj_database_url

# import psycopg2.extensions
from decouple import config
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

# import lz4
# ABSOLUTE_PATH = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
# MEDIA_ROOT = ABSOLUTE_PATH('media/')


DEFAULT_CHARSET = "utf-8"
VERSION = 1

ENV_NAME = "Clavem"
BASE_URL = "clavem.co:8000"
# https://www. mgbonum.com

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
PROJECT_DIR = Path(__file__).resolve(strict=True)

MANAGERS = [
    ("clvm", "mgb@clavem.co"),
    # ("mgb", "mgbonum@protonmail.com"),
    ("support", "support@clavem.co"),
]
ADMINS = MANAGERS

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    # 'grappelli',
    # 'filebrowser',
    "chat.apps.ChatConfig",
    "channels",
    "whitenoise.runserver_nostatic",
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    "django.contrib.staticfiles",
    "django.contrib.admin",  # 'essays.apps.EssaysAdminConfig', # overrided default admin
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    # # 'django.contrib.humanize',
    # # "sslserver",  # https://pypi.org/project/django-sslserver
    # "django_hosts",  # https://pypi.org/project/django-hosts
    "tailwind",
    "django_browser_reload",
    "theme",
    "django_extensions",  # https://pypi.org/project/django-extensions
    # "gdpr_assist",  # https://django-gdpr-assist.readthedocs.io/en/latest/installation.html
    # "gdpr",  # https://github.com/druids/django-GDPR
    "meta",  # https://pypi.org/project/django-meta
    # # "defender",  # https://django-defender.readthedocs.io/en/latest # downgrade django
    "corsheaders",  # https://pypi.org/project/django-cors-headers
    "compressor",
    "captcha",  # https://pypi.org/project/django-simple-captcha
    "mptt",  # https://django-mptt.readthedocs.io/en/latest/install.html
    # "rosetta",  # https://pypi.org/project/django-rosetta
    # "hitcount",
    # https://dj-hitcount.readthedocs.io/en/latest/installation.html
    # 'django_cleanup.apps.CleanupConfig',
    # "robots",  # https://pypi.org/project/django-robots
    # "admin_honeypot",  # https://pypi.org/project/django-admin-honeypot
    "widget_tweaks",  # https://pypi.org/project/django-widget-tweaks
    # "django_celery_beat",
    "django_celery_results",  # https://pypi.org/project/django-celery-results/
    "sslserver",  # https://github.com/teddziuba/django-sslserver
    "rest_framework",  # https://www.django-rest-framework.org/#installation
    "rest_framework.authtoken",
    "drfpasswordless",  # https://github.com/aaronn/django-rest-framework-passwordless
    "sorl.thumbnail",  # https://github.com/jazzband/sorl-thumbnail
    "tinymce",  # https://github.com/jazzband/django-tinymce
    # "newsletter",  # https://django-newsletter.readthedocs.io/en/latest/installation.html
    # "embed_video",
    # "blacklist",
    # 'pwa',# https://github.com/silviolleite/django-pwa
    # 'xicon',# https://pypi.org/project/django-xicon
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.github',
    # 'rest_auth',# pip install django-rest-auth
    # 'rest_auth.registration',# pip install django-registration
    # 'django_otp',
    # 'django_otp.plugins.otp_totp',# 'django_otp.plugins.otp_hotp',
    # 'django_otp.plugins.otp_static',
    # 'allauth_2fa',
    # 'pagedown.apps.PagedownConfig',
    # 'django.contrib.flatpages',
    # 'letsencrypt',#django-
    # https://django-simple-history.readthedocs.io/en/latest/quick_start.html
    # https://django-authority.readthedocs.io/en/latest/installation/
    # 'analytical',
    # 'djmoney',# https://github.com/django-money/django-money
    # 'tracking', # django-tracking2
    # 'django_user_agents',# https://pypi.org/project/django-user-sessions/
    # 'tracking_analyzer',
    # 'shortener',# https://pypi.org/project/django-link-shortener/
    # 'crispy_forms',# https://pypi.org/project/django-crispy-forms/
    # 'webpack_loader',
]
TAILWIND_APP_NAME = "theme"
WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
# MAX_ACTIVE_TASKS = 2

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}
# GRAPH_MODELS = {
#     "all_applications": True,
#     "group_models": True,
# }
# https://pypi.org/project/drfpasswordless/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    )
}
PASSWORDLESS_AUTH = {
    "PASSWORDLESS_AUTH_TYPES": ["EMAIL"],  # , "MOBILE"
    "PASSWORDLESS_EMAIL_NOREPLY_ADDRESS": "noreply@clavem.co",
    "PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME": "newsletter/common.html",
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# celery -A core beat -l INFO
CELERY_BEAT_SCHEDULE = {
    "scheduled_task": {
        "task": "home.tasks.add",
        "schedule": 5.0,
        "args": (1, 5),
    },
    "database": {
        "task": "home.tasks.bkup",
        "schedule": 5.0,
    },
}

# or set up admin/ Periodic task
# celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.db.DatabaseCache",
#         "LOCATION": "cachedb",
#     }
# }
# CELERY_RESULT_BACKEND = "django-cache"
# CELERY_TIMEZONE = "Australia/Tasmania"
# CELERY_TASK_TRACK_STARTED = True
# CELERY_TASK_TIME_LIMIT = 30 * 60

# HITCOUNT_KEEP_HIT_ACTIVE = {'days': 7}
# HITCOUNT_HITS_PER_IP_LIMIT = 1# 0 unlimited
# HITCOUNT_EXCLUDE_USER_GROUP = ('ADMINS',)# not used
# HITCOUNT_KEEP_HIT_IN_DATABASE = {'days': 30}

MIDDLEWARE = [
    # "django_hosts.middleware.HostsRequestMiddleware",  # https://pypi.org/project/django-hosts/
    "django.middleware.security.SecurityMiddleware",
    # 'tracking.middleware.VisitorCleanUpMiddleware',
    # 'tracking.middleware.VisitorTrackingMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # between sessions and common
    "corsheaders.middleware.CorsMiddleware",  # https://pypi.org/project/django-cors-headers/
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "blacklist.middleware.blacklist_middleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'adminrestrict.middleware.AdminPagesRestrictMiddleware',
    # "csp.middleware.CSPMiddleware",  # https://pypi.org/project/django-csp/
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # 'django_otp.middleware.OTPMiddleware',# django-two-factor-auth
    # 'allauth_2fa.middleware.AllauthTwoFactorMiddleware',
    # 'allauth_2fa.middleware.BaseRequire2FAMiddleware',
    # 'two_factor.middleware.threadlocals.ThreadLocals',
    # 'allauth.account.auth_backends.AuthenticationBackend',
    # "defender.middleware.FailedLoginMiddleware",
    # "django_hosts.middleware.HostsResponseMiddleware",
]
# https://docs.djangoproject.com/en/3.2/ref/contrib/messages/
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# https://django-embed-video.readthedocs.io/en/latest/installation.html
TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.request",)

# if DEBUG:
#     INSTALLED_APPS.append(
#         "debug_toolbar",
#     )  #'silk'
#     MIDDLEWARE.append(
#         "debug_toolbar.middleware.DebugToolbarMiddleware",
#     )  # https://pypi.org/project/django-debug-toolbar/
# 'silk.middleware.SilkyMiddleware'
# MIDDLEWARE += 'django.middleware.common.BrokenLinkEmailsMiddleware'
# # https://docs.djangoproject.com/en/3.2/howto/error-reporting/

ROOT_URLCONF = "core.urls"
# ROOT_HOSTCONF = "core.hosts" # django_hosts
# DEFAULT_HOST = "www"
DEFAULT_REDIRECT_URL = BASE_URL  # https
PARENT_HOST = BASE_URL  # "www.clavem.co:8000"
APPEND_SLASH = True
SITE_ID = 2  # django.contrib.sites
TEMPLATES_DIR = BASE_DIR / "templates"  # os.path.join(BASE_DIR, 'templates')
# FRONTEND_DIR = BASE_DIR / 'frontend'# vuejs

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATES_DIR,
        ],  # [os.path.join(VUE_UI_DIR, 'dist/templates'),], # Vue
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.from_settings",
                "shop.context_processors.menu_categories",
            ],
            # 'loaders': [
            #     'django.template.loaders.app_directories.Loader',
            #     ('django.template.loaders.cached.Loader', [
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',
            #         'path.to.custom.Loader',
            #     ]),
            # ],
        },
    },
]

# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": dj_database_url.config(
        default=config("DB_URL"),
        conn_max_age=600,
        ssl_require=True,
        engine="django.db.backends.postgresql",
    ),
    # "gdpr_log": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": BASE_DIR / "gdpr-log.sqlite3",
    # },
}
# https://docs.djangoproject.com/en/4.1/topics/testing/advanced/#topics-testing-advanced-multidb
if "test" in sys.argv:
    DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3"}
    # SOUTH_TESTS_MIGRATE = False
    # https://south.readthedocs.io/en/latest/installation.html#installation

# DATABASE_ROUTERS = ["gdpr_assist.routers.EventLogRouter"]

# docker-compose https://docs.docker.com/compose/django/
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }

#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DB_NAME"),
#         "USER": config("DB_USER"),
#         "PASSWORD": config("DB_PSW"),
#         "HOST": config("DB_HOST"),
#         "PORT": config("DB_PORT"),
#         "client_encoding": "UTF8",
#     },
#     "OPTIONS": {
#         "isolation_level": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
#     },
# 'extra': {# local db to store temporary files
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': PROJECT_DIR / 'temp-db.sqlite'
# }
# }
# DATABASE_POOL_CLASS = "sqlalchemy.pool.QueuePool"
# DATABASE_POOL_ARGS = {
#     "max_overflow": 10,
#     "pool_size": 5,
#     "recycle": 300,
# }
# Heroku postgresql database the following lines are NOT the best practices for production
# override local postgresql with heroku's
# DB_FROM_ENV = dj_database_url.config()  #'postgres://mgb:0utisTu5@127.0.0.1:5432/amgbdb'
# DATABASES["default"].update(DB_FROM_ENV)
# DATABASES["default"]["CONN_MAX_AGE"] = 500

# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {
            "user_attributes": ("email", "password", "first_name", "last_name"),
            "max_similarity": 0.7,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# https://github.com/jazzband/django-redis rediss://[[username]:[password]]@localhost:6379/0
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "rediss://127.0.0.1:6379/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # 'PASSWORD': "mysecret",
#             "PICKLE_VERSION": -1,  # Use the latest protocol version
#             "SOCKET_CONNECT_TIMEOUT": 5,  # seconds
#             "SOCKET_TIMEOUT": 5,
#             "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",  # zlib.ZlibCompressor
#             # import lzma# slower 'COMPRESSOR': 'django_redis.compressors.lzma.LzmaCompressor'
#             "IGNORE_EXCEPTIONS": True,
#         },
#         "KEY_PREFIX": "example",
#     }
# }
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_CACHE_ALIAS = 'default'
# DJANGO_REDIS_IGNORE_EXCEPTIONS = True
# DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
# DJANGO_REDIS_LOGGER = 'path/logger'# __name__ is default


DEBUG = config("DEBUG", default=False, cast=bool)

try:
    SECRET_KEY = config("SECRET_KEY")
except ImproperlyConfigured as ic:
    raise ImproperlyConfigured(_("SECRET_KEY environment variable is missing!")) from ic

ALLOWED_HOSTS = ["*"]  # config("ALLOWED_HOSTS").split(",")

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
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # (,)
# #support@clavem.co ENV_NAME + ' <support@' + BASE_URL + '>'# Customer Care


INSTALLED_APPS += [
    "home.apps.HomeConfig",
    # "chat",
    "accounts.apps.AccountsConfig",
    "essays.apps.EssaysConfig",
    "notes.apps.NotesConfig",
    "education.apps.EducationConfig",
    "team.apps.TeamConfig",
    "marketing.apps.MarketingConfig",
    "shop.apps.ShopConfig",
    "search.apps.SearchConfig",
    "tags.apps.TagsConfig",
    "carts.apps.CartsConfig",
    "addresses.apps.AddressesConfig",
    "billing.apps.BillingConfig",
    "orders.apps.OrdersConfig",
    "analytics.apps.AnalyticsConfig",
    "shorturl.apps.ShorturlConfig",
    # "ariadne.contrib.django",# "graphene_django",
]

AUTH_USER_MODEL = "accounts.CUser"

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
# X-Content-Type-Options
SECURE_CONTENT_TYPE_NOSNIFF = True
# Strict-Transport-Security
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# that requests over HTTP are redirected to HTTPS. also can config in webserver
SECURE_SSL_REDIRECT = True

# for more security
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Strict"

# django-cors-headers
CORS_ALLOWED_ORIGINS = ["https://js.stripe.com", "https://polyfill.io"]
# , "https://commerce.coinbase.com" CORS_ALLOWED_ORIGIN_REGEXES = [
#     #r"^https://\w+\.stripe\.com$",
# ]
CORS_ORIGIN_ALLOW_ALL = False
CORS_REPLACE_HTTPS_REFERER = False

# https://django-csp.readthedocs.io/en/latest/installation.html
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
    "https://openfpcdn.io/fingerprintjs/v3",
    # "https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js"
)  # "https://www.google.com/recaptcha/", "https://www.gstatic.com/recaptcha/",
# "https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.5.0/dist/alpine.min.js" "'nonce-lrEwC5VX0M'"
# "https://chimpstatic.com/mcjs-connected/js/users/0e61ec17658f41b70da7d62f5/
# 0a42a86cd2c1b1c3c4bc6025d.js",
# "https://hcaptcha.com", "https://*.hcaptcha.com",
# "https://polyfill.io/v3/polyfill.min.js",
# "https://cdnjs.cloudflare.com/ajax/libs/jsrender/1.0.6/jsrender.js",
# "https://cdn.jsdelivr.net/npm/marked/marked.min.js",
# "https://cdn.jsdelivr.net/npm/darkmode-js@1.5.6/lib/darkmode-js.min.js",
CSP_FRAME_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://polyfill.io/v3/polyfill.min.js",
    "https://commerce.coinbase.com/",
    "https://js.stripe.com",
    "https://hooks.stripe.com",
    "https://checkout.stripe.com",
)
# "https://www.google.com/recaptcha/", "https://hcaptcha.com", "https://*.hcaptcha.com",
# "https://cdn.jsdelivr.net/npm/darkmode-js@1.5.6/lib/darkmode-js.min.js"
CSP_CONNECT_SRC = ("'self'", "https://api.stripe.com", "https://checkout.stripe.com")
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    # "https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.css",
)  # "https://hcaptcha.com", "https://*.hcaptcha.com",
# "https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.css",
# "https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.css",
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

# HOST_SCHEME = "http://"  # https://
# SECURE_PROXY_SSL_HEADER = None
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_HSTS_SECONDS = 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# SECURE_FRAME_DENY = False
# SECURE_HSTS_PRELOAD = False

# smtp.gmail.com
# https://support.google.com/mail/answer/7126229?visit_id=637475480606318471-1042357849&rd=2#cantsignin
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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

TIME_ZONE = "UTC"
USE_TZ = True  # set dynamic time according to geolocalization
DATE_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M"
]  # https://docs.djangoproject.com/en/3.2/ref/settings/#date-input-formats
USE_I18N = True
USE_L10N = False

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# Static files (CSS, JavaScript, Images) https://docs.djangoproject.com/en/3.2/howto/static-files/
# STATIC_HOST = config('STATIC_HOST', '')
# http://whitenoise.evans.io/en/stable/django.html#use-a-content-delivery-network
# STATIC_URL = STATIC_HOST + '/static/'
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static_cdn"  # folder for collectstatic 'staticfiles'
# os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'static_root')
# #Path(__file__).resolve(strict=True).parent
# '/var/www/clavem.co/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    # FRONTEND_DIR / 'dist/static',
    # os.path.join(BASE_DIR, 'frontend/dist),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # "compressor.parser.LxmlParser",
    # "compressor.filters.cssmin.CSSCompressorFilter",
    "compressor.finders.CompressorFinder",
]

COMPRESS_ENABLED = True

# gzip functionality enabled pip install whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# STATICFILES_STORAGE = 'config.storage.S3Storage'# AWS docs

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

PROTECTED_ROOT = MEDIA_ROOT / "protected"
# os.path.join(os.path.dirname(BASE_DIR), "media", "protected_root")

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    # specific authentication methods, such as login by e-mail
    # 'allauth.account.auth_backends.AuthenticationBackend',
)

# TWO_FACTOR_FORCE_OTP_ADMIN = True
# https://django-two-factor-auth.readthedocs.io/en/stable/installation.html
LOGIN_URL = "/login/"  # 'two_factor:login'
LOGIN_REDIRECT_URL = "/"  # 'two_factor:profile'
LOGOUT_URL = "/logout/"
LOGOUT_REDIRECT_URL = "/"

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

# CAPTCHA_FONT_PATH = STATIC_URL + 'fonts/open-sans/OpenSans-Regular.ttf'
CAPTCHA_FONT_SIZE = 22
CAPTCHA_IMAGE_SIZE = (80, 40)
CAPTCHA_LETTER_ROTATION = None
# CAPTCHA_BACKGROUND_COLOR = '#ffffff'#'#f0f1f3'
# CAPTCHA_FOREGROUND_COLOR = '#000000'
CAPTCHA_CHALLENGE_FUNCT = "captcha.helpers.math_challenge"  # random_char_challenge'
# CAPTCHA_MATH_CHALLENGE_OPERATOR = '*'
CAPTCHA_NOISE_FUNCTIONS = ("captcha.helpers.noise_dots",)
# 'captcha.helpers.noise_arcs','captcha.helpers.noise_null',


# https://django-allauth.readthedocs.io/en/latest/advanced.html

# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'none'


# django.registration accounts/models EmailActivationQuerySet
ACCOUNT_ACTIVATION_DAYS = 7  # the user has 1 week to activate the account

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # 'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     ]
# }
#     # 'DEFAULT_PERMISSION_CLASSES': (
#     #     'rest_framework.permissions.IsAuthenticated',
#     # ),
#     # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     # 'PAGE_SIZE': 2
# }

# BDEA_MESSAGE = _("Please add a valid email.")

# https://django-newsletter.readthedocs.io/en/latest/settings.html
# NEWSLETTER_THUMBNAIL = "sorl-thumbnail"
# NEWSLETTER_CONFIRM_EMAIL = False
# # django-imperavi "imperavi.widget.ImperaviWidget"
# NEWSLETTER_RICHTEXT_WIDGET = "tinymce.widgets.TinyMCE"

# # # Amount of seconds to wait between each email. Here 50ms is used.
# NEWSLETTER_EMAIL_DELAY = 0.05

# # # Amount of seconds to wait between each batch. Here 30 seconds is used.
# NEWSLETTER_BATCH_DELAY = 30

# # # Number of emails in one batch
# NEWSLETTER_BATCH_SIZE = 100


# https://us19.admin.mailchimp.com/account/api/ # lists/settings/defaults?id=321186

MAILCHIMP_API_KEY = config("MAILCHIMP_API_KEY")
MAILCHIMP_DATA_CENTER = config("MAILCHIMP_DATA_CENTER")
MAILCHIMP_EMAIL_LIST_ID = config("MAILCHIMP_EMAIL_LIST_ID")
MAILCHIMP_SUBSCRIBE_LIST_ID = config("MAILCHIMP_SUBSCRIBE_LIST_ID")


# https://stripe.com/docs https://us19.admin.mailchimp.com/lists/ settings list name and defaults

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = config("STRIPE_PUB_KEY")


# ACCOUNT_ADAPTER = 'allauth_2fa.adapter.OTPAdapter'
# ACCOUNT_TEMPLATE_EXTENSION = 'html'
# ALLAUTH_2FA_ALWAYS_REVEAL_BACKUP_TOKENS = True

TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "cleanup_on_startup": True,
    "custom_undo_redo_levels": 20,
    "selector": "textarea",
    "theme": "silver",
    "plugins": """
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen insertdatetime nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists charmap print hr
            anchor pagebreak
            """,
    "toolbar1": """
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            """,
    "toolbar2": """
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor | code |
            """,
    "contextmenu": "formats | link image",
    "fontsize_formats": "8pt 9pt 10pt 11pt 12pt 14pt 18pt 24pt 30pt 36pt 48pt 60pt 72pt 96pt",
    # 'content_css' : STATIC_URL + 'css/custom_tinycme.css',
    "menubar": True,
    "statusbar": True,
}
# TINYMCE_JS_URL = STATIC_URL / '/tiny_mce/tiny_mce.js'# TINYMCE_JS_ROOT = MEDIA_ROOT /
# TINYMCE_COMPRESSOR = True


# IAM Management Console

# AWS_GROUPNAME = ''
# AWS_USERNAME = ''
# AWS_ACCESS_KEY_ID = ''
# AWS_SECRET_KEY = ''


# tracking2
# TRACK_AJAX_REQUESTS = True
# TRACK_ANONYMOUS_USERS = True
# TRACK_SUPERUSERS = False
# TRACK_PAGEVIEWS = True


# https://towardsdatascience.com/productionize-a-machine-learning-model-with-a-django-api-c774cb47698c
# MODELS = BASE_DIR / 'dl/models'


# MARKDOWN_DEUX_STYLES = {'default': {
#     "extras": {
#         "code-friendly": None,
#     },
#     "safe_mode": False,
# }}

# Vue
# WEBPACK_LOADER = {
#     'DEFAULT': {
#         'CACHE': not DEBUG,
#         'BUNDLE_DIR_NAME': 'dist/',
#         'STATS_FILE': FRONTEND_DIR / 'webpack-stats.json',
#     }
# }

# metadata https://django-meta.readthedocs.io/en/latest/views.html
META_SITE_PROTOCOL = "https"  # https
META_SITE_DOMAIN = BASE_URL
META_SITE_TYPE = ""
META_SITE_NAME = ENV_NAME

# Items will stay in the cart for 24 hours
SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = "cart"

# django_heroku.settings(locals(), staticfiles=False)

# https://docs.djangoproject.com/en/3.2/topics/i18n/# Add Chinese, Espanol
LANGUAGE_CODE = "en"  # -us
LANGUAGES = (
    ("en", _("English")),
    ("de", _("German")),
    # ("ja", u"日本語"),
    ("it", _("Italian")),
    ("fr", _("French")),
    ("es", _("Spanish")),
    # ('zh-CN', u'简体中文'),#Simplified Chinese
    # ('zh-TW', u'繁體中文'),#Traditional
)

# RECAPTCHAV3_SECRET = config('RECAPTCHAV3_SECRET')# google
# HCAPTCHA_SECRET_KEY = config('HCAPTCHA_SECRET_KEY')
# VERIFY_URL = config('VERIFY_URL', default='https://hcaptcha.com/siteverify')

# filebrowser
# FILEBROWSER_DIRECTORY =
# DIRECTORY = getattr(settings, 'FILEBROWSER_DIRECTORY', 'uploads/')

# https://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
# CRISPY_TEMPLATE_PACK = 'bootstrap4'  # 'uni_form' issue with tailwind

# SHORTENER_ENABLE_TEST_PATH = False
# SHORTENER_ENABLED = True
# SHORTENER_MAX_URLS = -1
# SHORTENER_MAX_CONCURRENT = -1
# SHORTENER_LIFESPAN = -1
# SHORTENER_MAX_USES = -1

# GEOIP_PATH = 'geoip'
# TRACKING_ANALYZER_MAXMIND_COUNTRIES = 'GeoLite2-Country_20200728.tar.gz'
# TRACKING_ANALYZER_MAXMIND_CITIES = 'GeoLite2-City_20200728.tar.gz'#29MB

# CHARTBEAT_USER_ID = '12345'
# CLICKMAP_TRACKER_CODE = '912'
# CLICKY_SITE_ID = 'xxxxxxxx'
# CRAZY_EGG_ACCOUNT_NUMBER = 'xxxxxxxx'# $249/mo*
# FACEBOOK_PIXEL_ID = '1234567890'
# GAUGES_SITE_ID = '0123456789abcdef0123456789abcdef'
# GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-1234567-8'
# HUBSPOT_PORTAL_ID = '1234'
# HUBSPOT_DOMAIN = 'somedomain.web101.hubspot.com'
# INTERCOM_APP_ID = '0123456789abcdef0123456789abcdef01234567'
# KISS_INSIGHTS_ACCOUNT_NUMBER = '12345'
# KISS_INSIGHTS_SITE_CODE = 'abc'
# KISS_METRICS_API_KEY = '0123456789abcdef0123456789abcdef01234567'
# MATOMO_DOMAIN_PATH = 'your.matomo.server/optional/path'
# MATOMO_SITE_ID = '123'
# MIXPANEL_API_TOKEN = '0123456789abcdef0123456789abcdef'
# OLARK_SITE_ID = '1234-567-89-0123'
# OPTIMIZELY_ACCOUNT_NUMBER = '1234567'
# PERFORMABLE_API_KEY = '123abc'
# WOOPRA_DOMAIN = 'abcde.com'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
