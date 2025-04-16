# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-


"""Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their config, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from os.path import join
from typing import Tuple

from django.utils.translation import gettext_lazy as _
from import_export.formats.base_formats import CSV, XLSX

from config.settings.components import PROJECT_PATH, env

#
# ADMIN SETTINGS
# ------------------------------------------------------------------------------
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')
AUTH_USER_MODEL = 'database.UserORM'
LOGIN_REDIRECT_URL = '/admin/'
LOGIN_URL = 'account_login'
USERNAME_BLACKLIST = ['vicobits', 'admin']

DJANGO_APPS: Tuple[str, ...] = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'django.contrib.postgres',
    # Useful template tags:
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS: Tuple[str, ...] = (
    # Security:
    'constance',
    # API Rest
    'corsheaders',
    'rest_framework',
    'rest_framework_api_key',
    # 'rest_framework_simplejwt.token_blacklist',
    # Models
    'phonenumber_field',
    'django_json_widget',
    'tinymce',
    'import_export',
    # Assets
    'tailwind',
    'imagekit',
    'django_browser_reload',
    'django_jsonform',
)

LOCAL_APPS: Tuple[str, ...] = (
    'src.auth.presentation.app.AuthConfig',
    'src.common.database.app.DatabaseConfig',
    'src.common.presentation.app.CommonConfig',
    'src.notifications.presentation.app.NotificationsConfig',
    'src.pending_actions.presentation.app.PendingActionsConfig',
    'src.tenants.presentation.app.TenantsConfig',
    'src.users.presentation.app.UsersConfig',
    'src.web.app.WebConfig',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE: Tuple[str, ...] = (
    'src.common.presentation.middleware.DeactivatedDisallowedHost',
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'djangorestframework_camel_case.middleware.CamelCaseMiddleWare',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
)

# URL CONFIGURATION
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
SITE_ID = 1
MIGRATION_MODULES = {
    'sites': 'src.common.database.sites.migrations',
}

# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
LOCALE_PATHS = [
    join(PROJECT_PATH, 'locale'),
]

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (join(PROJECT_PATH, 'fixtures'),)

#
#  ~ NOTIFICATIONS
#
EMAIL_BACKEND = env(
    'DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST, EMAIL_PORT = '127.0.0.1', 1025  # Work with MailHog
DEFAULT_FROM_EMAIL = env(
    'DJANGO_DEFAULT_FROM_EMAIL', default='Xiberty <noreply@mail.collectives.pro>'
)
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default='Reports <server@mail.collectives.pro>')
WHATSAPP_API_KEY = env('WHATSAPP_API_KEY')
WHATSAPP_API_HOSTNAME = env('WHATSAPP_API_HOSTNAME')

WHATSAPP_API_SESSION_WEBHOOK = env('WHATSAPP_API_SESSION_WEBHOOK')
WHATSAPP_API_SESSION_API_KEY = env('WHATSAPP_API_SESSION_API_KEY')

# TEMPLATES CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(PROJECT_PATH, 'web/templates'),
        ],
        'OPTIONS': {
            'debug': False,
            'loaders': [
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.filesystem.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Custom context processor
                'src.common.presentation.context_processors.website',
            ],
        },
    }
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_HTDOCS_PATH = env('DJANGO_HTDOCS_PATH', default=join(PROJECT_PATH, 'public'))
STATIC_ROOT = join(DJANGO_HTDOCS_PATH, 'static')
STATIC_URL = '/static/'
# STATICFILES_DIRS = (join(PROJECT_PATH, 'web/static'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
MEDIA_ROOT = join(DJANGO_HTDOCS_PATH, 'media')
MEDIA_URL = '/media/'

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

#
# AUTHENTICATION CONFIGURATION
# https://docs.djangoproject.com/en/2.2/topics/auth/
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'src.common.presentation.auth_backends.SimpleEmailBackend',
)

# EXTRA CONFIGURATION
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000
PAGINATION_PAGE_SIZE = 50
TOKEN_EXPIRATION_DAYS = env.int('DJANGO_TOKEN_EXPIRATION_DAYS', default=7)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Security
# https://docs.djangoproject.com/en/2.2/topics/security/

SESSION_COOKIE_HTTPONLY = True
# enable/disable the CSRF Token reading by the client-side
CSRF_COOKIE_HTTPONLY = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy#Syntax
REFERRER_POLICY = 'no-referrer'

# Timeouts
EMAIL_TIMEOUT = 5

#
# IMPORT - EXPORT
#
IMPORT_FORMATS = [CSV, XLSX]
EXPORT_FORMATS = [XLSX]

# PLATFORM SETTINGS
# ------------------------------------------------------------------------------
FAVICON_PATH = STATIC_URL + 'favicon.ico'
PROJECT_SUPPORT_EMAIL = 'support@collectives.pro'

ADMINS = (('Support', PROJECT_SUPPORT_EMAIL),)
MANAGERS = ADMINS
PROJECT_NAME = 'Reminders API'

API_HOSTNAME = env('API_HOSTNAME')
BACKOFFICE_HOSTNAME = env('BACKOFFICE_HOSTNAME')
PAGES_ROOT_HOSTNAME = env('PAGES_ROOT_HOSTNAME')

PROJECT_SERVE_STATIC = env.bool('DJANGO_SERVE_STATIC', default=False)
PROJECT_AUTHOR = 'Support <{0}>'.format(PROJECT_SUPPORT_EMAIL)
PROJECT_OWNER = 'Reminders'
PROJECT_OWNER_DOMAIN = API_HOSTNAME
PROJECT_DESCRIPTION = 'X Platform'
PROJECT_SUPPORT_PHONE = '(+52) 550011223344'
PROJECT_TERMS_URL = '{0}/terms'.format(API_HOSTNAME)

TAILWIND_APP_NAME = 'src.web'
