# -*- coding: utf-8 -*-

from local_settings import *


LOGGING.update({
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admin': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
})

MANAGERS = ADMINS


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.

LANGUAGE_CODE = 'fa-IR'
TIME_ZONE = 'Iran'
AUTH_USER_MODEL = 'accounts.JuckUser'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = BASEPATH + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"

MEDIA_URL = SITE_URL + 'media/'

UPLOAD_URL = 'uploads'
UPLOAD_ROOT = MEDIA_ROOT + 'uploads'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/me'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT   = BASEPATH + 'static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_ROOT = ''
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    BASEPATH + '/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

CAPTCHA_LENGTH = 6

def generate_captcha():
    import random

    words_list = [u'ا', u'ب', u'پ', u'ت', u'س', u'ج', u'چ', u'ه', u'خ', u'د', u'ذ', u'ر', u'ز', u'ژ', u'س', u'ش',
                  u'ص', u'ض', u'ط', u'ظ', u'ع', u'غ', u'ف', u'ق', u'ک', u'گ', u'ل', u'م', u'ن', u'و', u'ه', u'ی',
    ]

    captcha = u''
    for i in range(CAPTCHA_LENGTH):
        captcha += words_list[random.randint(0, len(words_list) - 1)]

    return captcha, captcha[::-1]


#CAPTCHA_CHALLENGE_FUNCT = generate_captcha
PROJECT_INAGURATION_YAER = 1392

from datetime import datetime

PROJECT_INAGURATION_EXACT_DATE = datetime.utcfromtimestamp(0)

CAPTCHA_NOISE_FUNCTIONS = ()
CAPTCHA_BACKGROUND_COLOR = '#4EAEE5'
CAPTCHA_LETTER_ROTATION = (-20, 20)
#CAPTCHA_FONT_PATH = BASEPATH + '/static/fonts/BYekan.ttf'



# Bejes zuck it, I did this task, ha ha ha :D
#TODO => Boji ( The R&D Guy ) - Gmail works, see if there's sth better :-bd


EMAIL_USE_TLS = True
#EMAIL_SENDER = 'BojasWillFindSthCool.com'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'juck.system@gmail.com'
EMAIL_SENDER  = 'juck.system@gmail.com'
EMAIL_HOST_PASSWORD = 'SadeghiSinaFJBejes'
EMAIL_PORT = 587

SITE_URL = 'http://127.0.0.1:8000/'

RESULTS_PER_PAGE = 2

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k_2g%nx&10-jq$BejesritdoYou2n9&=-bxc*pvSuck1uf(d&*a^kumFjoq+bs|t;h-Bit0t^@I*chIy=fre~30!a+%kna/y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',

)
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

AUTHENTICATION_BACKENDS = ('accounts.auth.JuckAuthenticationBackend',)

ROOT_URLCONF = 'juck.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'juck.wsgi.application'

TEMPLATE_DIRS = (BASEPATH + '/templates',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'captcha',
    'crumbs',
    # 'debug_toolbar',
    'accounts',
    'image',
    'log',
    'news',
    'articles',
    'question',
    'requests',
    'comments',

    'httplib2', #    These 4 are
    'openid', #      what u need to
    'oauth2', #      integrate social_auth plug
    'social_auth',# in your GAE project

)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
                        "django.core.files.uploadhandler.TemporaryFileUploadHandler",)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.github.GithubBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "social_auth.context_processors.social_auth_by_type_backends",
    'django.contrib.auth.context_processors.auth'
)

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'github')

GITHUB_API_KEY = ''
GITHUB_API_SECRET = ''

GOOGLE_OAUTH2_CLIENT_ID = '524830416483-pddbupi0qf5eoapq2q1vdi25q93mm6cc.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'yTsABLiLfsN3Qkqcyq058JmM'
