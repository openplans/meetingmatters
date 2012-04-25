# Django settings for publicmeeting project.

import os.path

try:
    from . import local
except ImportError:
    local = None

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_local(varname, default=None):
    """
    Go through the various places where local, potentially sensitive variables
    are stored.  This ranges from environment variables on Heroku, to an
    environment file on Dotcloud, to a local module on a development server.

    """
    # Try the local module first.
    try:
        return getattr(local, varname)
    except AttributeError:
        pass

    # Try the os environment.
    import os
    try:
        return os.environ[varname]
    except KeyError:
        pass

    # Heroku DATABASE_URL-based DB configuration.
    if varname == 'DATABASES':
        dbs = {}

        def parse_db_url(url_string, spatial=False):
            import urlparse
            url = urlparse.urlparse(url_string)

            # Ensure default database exists.
            scheme_to_engine = {
                'postgres': ('django.db.backends.postgresql_psycopg2'
                             if not spatial else
                             'django.contrib.gis.db.backends.postgis'),
                'mysql': 'django.db.backends.mysql',
            }

            return {
                'ENGINE': scheme_to_engine[url.scheme],
                'NAME': url.path[1:],
                'USER': url.username,
                'PASSWORD': url.password,
                'HOST': url.hostname,
                'PORT': url.port,
            }

        if 'DATABASE_URL' in os.environ:
            dbs['default'] = parse_db_url(os.environ['DATABASE_URL'])

        elif 'SPACIALDB_URL' in os.environ:
            dbs['default'] = parse_db_url(os.environ['SPACIALDB_URL'], spatial=True)

        return dbs

    # If we get here and no default is supplied, raise an exception.
    if default is None:
        raise Exception('No value supplied for variable "' + str(varname) + '"')

    return default


DEBUG = True if get_local('DEBUG', True) in ('True', True) else False
TEMPLATE_DEBUG = True if get_local('TEMPLATE_DEBUG', DEBUG) in ('True', True) else False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = get_local('DATABASES', {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
})

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_local('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',

    'project.context_processors.regions',
    'utils.context_processors.settings.DEBUG',
    'utils.context_processors.settings.TEMPLATE_DEBUG',
    'utils.context_processors.site',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # These are for managing revisions.  The RevisionMiddleware wraps each
    # request in a revision.  Any changes to models in a request will count
    # under that revision.
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

ROOT_URLCONF = 'project.urls'

###############################################################################
#
# Static File Precompilation
#

COMPRESS_ENABLED = True  # set to ``not DEBUG`` by default

# Since we want to precompile our project's LESS against Bootstrap, we must
# specify the location of Bootstrap's less files in the lessc command.
BOOTSTRAP_LESS_DIR = os.path.join(PROJECT_PATH, '../../.env/lib/python2.7/site-packages/bootstrapped/static/less/')
LESSC_PATH = os.path.abspath(os.path.join(PROJECT_PATH, '../../node_modules/less/bin/lessc'))
COMPRESS_PRECOMPILERS = (
    ('text/less', LESSC_PATH + ' {infile} {outfile} -I' + BOOTSTRAP_LESS_DIR),
)

# So that the relative paths stay the same in our LESS as in our compiled CSS,
# dump the compiled/compressed files into the STATIC_URL directory.
#COMPRESS_OUTPUT_DIR = '.'

###############################################################################
#
# Authentication
#

AUTHENTICATION_BACKENDS = (
    # See http://django-social-auth.readthedocs.org/en/latest/configuration.html
    # for list of available backends.
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/'

###############################################################################
#
# 3rd-party service configuration and keys
#

TWITTER_CONSUMER_KEY         = get_local('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET      = get_local('TWITTER_CONSUMER_SECRET')

###############################################################################
#
# Site search configuration
#

SHORTEN_MODELS = {
    'm': 'meetings.meeting',
}
#SHORT_BASE_URL = 'http://mtm.tt/'

###############################################################################
#
# Applications
#

COMMUNITY_APPS = (
    'south',
    'django_nose',
    'debug_toolbar',
    'social_auth',
    'bootstrapped',
    'uni_form',
    'taggit',
    'taggit_templatetags',
    'compressor',
    'reversion',
    'shorturls',
    'djangorestframework',
    'floppyforms',
)

MY_REUSABLE_APPS = (
    'datetime_fields',
    'utils',
)

PROJECT_APPS = (
    'project',
    'meetings',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.gis',
) + PROJECT_APPS + MY_REUSABLE_APPS + COMMUNITY_APPS

################################################################################
#
# Testing and administration
#

# Tests (nose)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

# Debug toolbar
def custom_show_toolbar(request):
    return DEBUG
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'INTERCEPT_REDIRECTS': False
}
INTERNAL_IPS = ('127.0.0.1',)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
