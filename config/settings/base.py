"""
Base settings to build other settings files upon.
"""
import time
from pathlib import Path

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = ROOT_DIR / "medusa_website"  # medusa_website/
FRONTEND_DIR = Path(ROOT_DIR, "frontend")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", default=False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Australia/Melbourne"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = False
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "NAME": "medusa_website",
        "ENGINE": "django.db.backends.postgresql",
        "DATABASE_URL": "postgres://localhost/medusa_website",
        "USER": env("DATABASE_USER", default="postgres"),
        "PASSWORD": env("DATABASE_PASSWORD", default=None),
        "HOST": "localhost",
    }
    # "default": {
    #     "NAME": ROOT_DIR / "db.sqlite3",
    #     "ENGINE": "django.db.backends.sqlite3",
    # }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    # "djangocms_admin_style",  # https://github.com/django-cms/djangocms-admin-style
    "django.contrib.admin",
    "django.forms",
    "django.contrib.sitemaps",
]
THIRD_PARTY_APPS = [
    # "webpack_loader",
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    "imagekit",
    "cuser",
    "pg_copy",
    "bootstrap_modal_forms",
    "widget_tweaks",
    "django_tables2",
    "django_extensions",
    "bootstrap3",
    "django_filters",
    "extra_views",
    "martor",
    "pipeline",
    "colorfield",
    "tinymce",
    "memoize",
    "django_celery_results",
    "django_celery_beat",
]

LOCAL_APPS = [
    "medusa_website.users.apps.UsersConfig",
    "medusa_website.mcq_bank.apps.McqBankConfig",
    "medusa_website.osce_bank.apps.OSCEBankConfig",
    "medusa_website.org_chart.apps.OrgChartConfig",
    "medusa_website.frontend.apps.FrontendConfig",
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "medusa_website.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "medusa_website.utils.custom_middleware.SimpleMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = Path(ROOT_DIR / "static")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR / "static"),
    str(ROOT_DIR / "assets"),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [
            Path(APPS_DIR, "templates"),
        ],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "medusa_website.utils.context_processors.settings_context",
            ],
            "libraries": {
                "template_filters": "medusa_website.org_chart.templatetags.template_filters",
            },
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = False
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "medusa_website.gmailapi_backend.mail.GmailBackend"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL", default="website@medusa.org.au")
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[MeDUSA Website]")

# Gmail-specific settings
MEMBERLIST_EMAIL = "it@medusa.org.au"
GMAIL_CREDENTIALS_PATH = Path(env("GMAIL_CREDENTIALS_PATH")).resolve()
GMAIL_SCOPES = ["https://mail.google.com/"]

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Chris Culhane""", "it@medusa.org.au")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "logfile": {
            "class": "logging.FileHandler",
            "filename": str(ROOT_DIR / "logs/server.log"),
            "level": "INFO",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "logfile"]},
    "loggers": {
        "django": {
            "handlers": ["logfile", "logfile"],
        },
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console", "logfile"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console", "logfile"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_UNIQUE_EMAIL = True

# https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-user-models
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_VALIDATORS = "medusa_website.users.validators.CustomEmailValidator"

# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "medusa_website.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "medusa_website.users.adapters.SocialAccountAdapter"
ACCOUNT_MAX_EMAIL_ADDRESSES = 2
ACCOUNT_SIGNUP_REDIRECT_URL = "frontend:resources"

### CACHING
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-CACHE_MIDDLEWARE_ALIAS
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_KEY_PREFIX = ""
CACHE_MIDDLEWARE_SECONDS = 60  # in seconds

# MESSAGES
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Your stuff...
# ------------------------------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = [""]  # Over-ridden in other configs
APPEND_SLASH = True
# CORS_ALLOWED_ORIGINS = ("http://localhost:3000",)
CSRF_TRUSTED_ORIGINS = ["localhost:3000", ".medusa.org.au", ".medusa.org.au", "localhost:8000"]

# JAVASCRIPT LOADING
# https://django-pipeline.readthedocs.io/en/latest/configuration.html
PIPELINE = {
    # "PIPELINE_ENABLED": False,
    "PIPELINE_COLLECTOR_ENABLED": True,
    "CSS_COMPRESSOR": "pipeline.compressors.yuglify.YuglifyCompressor",
    "JS_COMPRESSOR": "pipeline.compressors.yuglify.YuglifyCompressor",
    "YUGLIFY_BINARY": env("YUGLIFY_BINARY", default=None),
    "JAVASCRIPT": {
        "js_core": {  # The order matters!
            "source_filenames": (
                "modules/core/jquery-3.5.1.min.js",
                "modules/core/popper.min.js",
                "modules/core/bootstrap-4.0.0.min.js",
            ),
            "output_filename": "pipeline/js/core.js",
        },
        "js_bootstrap_modal_forms": {
            "source_filenames": ("modules/bootstrap-modal-forms/*.js",),
            "output_filename": "pipeline/js/bootstrap-modal-forms.js",
        },
        "js_stats": {
            "source_filenames": ("js/project.js", "js/index.js"),
            "output_filename": "pipeline/js/stats.js",
        },
        "js_tablesorter": {
            "source_filenames": ("modules/tablesorter/dist/js/jquery.tablesorter.combined.js",),
            "output_filename": "pipeline/js/tablesorter.js",
        },
        "js_juicer": {
            "source_filenames": ("modules/juicer/*.js",),
            "output_filename": "pipeline/js/juicer.js",
        },
        "js_martor": {
            "source_filenames": ("modules/martor/js/*.js",),
            "output_filename": "pipeline/js/martor.js",
        },
    },
    "STYLESHEETS": {
        "css_core": {
            "source_filenames": ("modules/core/*.css", "sass/*.scss"),
            "output_filename": "pipeline/css/core.css",
        },
        "css_tablesorter": {
            "source_filenames": (
                "modules/tablesorter/dist/css/scss/*.scss",
                "modules/tablesorter/dist/css/theme.metro-dark.min.css",
            ),
            "output_filename": "pipeline/css/tablesorter.css",
        },
        "css_juicer": {
            "source_filenames": ("modules/juicer/*.css",),
            "output_filename": "pipeline/css/juicer.css",
        },
        "css_martor": {
            "source_filenames": ("modules/martor/css/*.css",),
            "output_filename": "pipeline/css/martor.css",
        },
    },
    "COMPILERS": ("libsasscompiler.LibSassCompiler",),
}

# https://github.com/sonic182/libsasscompiler

# WEBPACK_LOADER = {
#     "DEFAULT": {
#         "CACHE": not DEBUG,
#         "BUNDLE_DIR_NAME": "webpack_bundles/",  # must end with slash
#         "STATS_FILE": (ROOT_DIR / "webpack-stats.json").as_posix(),
#         "TIMEOUT": None,
#         "IGNORE": [r".+\.hot-update.js", r".+\.map"],
#         "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
#     },
# }

MEMBERLIST_XLSX = Path(MEDIA_ROOT, "users", "Club Weekly Membership Report Shedule.xlsx")
MEMBERLIST_CSV = Path(MEDIA_ROOT, "users", "memberlist.csv")
PG_COPY_BACKUP_PATH = Path(ROOT_DIR, "db_backup")

CRISPY_FAIL_SILENTLY = not DEBUG

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap-responsive.html"
PAGEDOWN_IMAGE_UPLOAD_ENABLED = False

# MARTOR CONFIG
# ----------------------
# https://github.com/agusmakmun/django-markdown-editor
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = {
    "emoji": "true",  # to enable/disable emoji icons.
    "imgur": "false",  # to enable/disable imgur/custom uploader.
    "mention": "false",  # to enable/disable mention
    "jquery": "true",  # to include/revoke jquery (require for admin default django)
    "living": "true",  # to enable/disable live updates in preview
    "spellcheck": "false",  # to enable/disable spellcheck in form textareas
    "hljs": "false",  # to enable/disable hljs highlighting in preview
}
# To show the toolbar buttons
MARTOR_TOOLBAR_BUTTONS = [
    "bold",
    "italic",
    "horizontal",
    "heading",
    # "pre-code",
    "blockquote",
    "unordered-list",
    "ordered-list",
    "link",
    "image-link",
    "image-upload",
    "emoji",
    # "direct-mention",
    "toggle-maximize",
    "help",
]
# Upload to locale storage
MARTOR_UPLOAD_PATH = STATIC_ROOT / f'images/uploads/{time.strftime("%Y/%m/%d/")}'
MARTOR_UPLOAD_URL = "/api/uploader/"  # change to local uploader
MARTOR_ENABLE_LABEL = True
# Maximum Upload Image in bytes
MAX_IMAGE_UPLOAD_SIZE = 5242880  # 5MB
# MARTOR_ALTERNATIVE_JQUERY_JS_FILE = None  # "jquery/dist/jquery.min.js"        # default None

# TINYMCE
# Used for HTML editing/preview for org_chart/subcommittee/
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 800,
    "menubar": "edit view insert format tools table tc help",
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | help",
}

TINYMCE_SPELLCHECKER = False
USE_COMPRESSOR = False
USE_EXTRA_MEDIA = False
USE_SPELLCHECKER = False
USE_FILEBROWSER = False

GOOGLE_RECAPTCHA_SECRET_KEY = env("GOOGLE_RECAPTCHA_SECRET_KEY", default=None)

# CELERY
CELERY_TIMEZONE = "Australia/Melbourne"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 10 * 60
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "django-db"
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
