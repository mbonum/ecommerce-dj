from pathlib import Path
from decouple import config

import dj_database_url

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
PROJECT_DIR = Path(__file__).resolve(strict=True)
SECRET_KEY = config("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")
DEFAULT_CHARSET = "utf-8"
VERSION = 1
ENV_NAME = "Clavem"
BASE_URL = "https://www.clavem.co"
MANAGERS = [
    ("mgb", "mgb@clavem.co"),
    ("support", "support@clavem.co"),
]
ADMINS = MANAGERS
INTERNAL_IPS = ["127.0.0.1", "localhost"]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "store",
    "graphene_django",
    "mptt"
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]
ROOT_URLCONF = "core.urls"
ROOT_HOSTCONF = "core.hosts"
DEFAULT_HOST = "www"
DEFAULT_REDIRECT_URL = BASE_URL
PARENT_HOST = BASE_URL
APPEND_SLASH = True
TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATES_DIR,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.from_settings"
            ],
        },
    },
]
WSGI_APPLICATION = "core.wsgi.application"
DATABASES = {
    "default": dj_database_url.config(
        default=config("DB_URL"),
        conn_max_age=600,
        ssl_require=True,
        engine="django_postgrespool2"
    )
}
DATABASE_POOL_CLASS = "sqlalchemy.pool.QueuePool"
DATABASE_POOL_ARGS = {
    "max_overflow": 10,
    "pool_size": 5,
    "recycle": 300
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {
            "user_attributes": ("email", "password", "first_name", "last_name"),
            "max_similarity": 0.7
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 10
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 'PASSWORD': 'mysecret',
            "PICKLE_VERSION": -1,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
            "IGNORE_EXCEPTIONS": True,
        },
        "KEY_PREFIX": "clvm",
    }
}
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher"
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
DATE_INPUT_FORMATS = ["%Y-%m-%d %H:%M"]
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (BASE_DIR / "locale",)
STATIC_URL = "/static/"
# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media/"

# REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"]}

# AWS_GROUPNAME = ''
# AWS_USERNAME = ''
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_KEY = env('AWS_SECRET_KEY')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACT = None

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
STATICFILES_DIRS = (BASE_DIR / "static",)

# DEFAUL_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DEFENDER_ACCESS_ATTEMPT_EXPIRATION = 24

CORS_ORIGIN_ALLOW_ALL = False
CORS_REPLACE_HTTPS_REFERER = True
CSP_DEFAULT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'"
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://hcaptcha.com",
    "https://*.hcaptcha.com",
    "https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.5.0/dist/alpine.min.js",
    "https://js.stripe.com",
    "https://cdn.jsdelivr.net/npm/darkmode-js@1.5.6/lib/darkmode-js.min.js"
)  # "https://chimpstatic.com/mcjs-connected/js/users/0e61ec17658f41b70da7d62f5/0a42a86cd2c1b1c3c4bc6025d.js", "https://hcaptcha.com/*", "https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js", "https://chimpstatic.com/mcjs-connected/js/users/0e61ec17658f41b70da7d62f5/0a42a86cd2c1b1c3c4bc6025d.js", "https://polyfill.io/v3/polyfill.min.js", "https://cdn.jsdelivr.net/npm/jquery@3.4.1/dist/jquery.min.js", "'https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.js", "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js", "https://unpkg.com/@popperjs/core@2", "https://cdnjs.cloudflare.com/ajax/libs/jsrender/1.0.6/jsrender.js", "https://cdn.jsdelivr.net/npm/marked/marked.min.js",
CSP_FRAME_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://hcaptcha.com",
    "https://*.hcaptcha.com",
    "https://js.stripe.com",
    "https://hooks.stripe.com",
    "https://cdn.jsdelivr.net/npm/darkmode-js@1.5.6/lib/darkmode-js.min.js"
)
CSP_CONNECT_SRC = (
    "'self'",
    "https://api.stripe.com"
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://hcaptcha.com",
    "https://*.hcaptcha.com"
)  # "https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.css", "https://cdnjs.cloudflare.com/ajax/libs/jquery-confirm/3.3.2/jquery-confirm.min.css",
CSP_FONT_SRC = ("'self'",)
CSP_IMG_SRC = (
    "'self'",
)  # "https://i.creativecommons.org/l/by-nc-nd/4.0/80x15.png" "'strict-dynamic'", "'https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif'", "'https://www.paypal.com/en_IT/i/scr/pixel.gif'",
CSP_MEDIA_SRC = ("'self'",)

HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = None  # ssl no longer secure ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 0  # 1000000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_HSTS_PRELOAD = True

# TRACK_AJAX_REQUESTS = True
# TRACK_ANONYMOUS_USERS = True
# TRACK_SUPERUSERS = False
# TRACK_PAGEVIEWS = True

META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = BASE_URL
META_SITE_TYPE = ENV_NAME + "website"
META_SITE_NAME = ENV_NAME