import os
# Django settings for opendata project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('OpenData Admins', 'admin@example.org'),
)
CONTACT_EMAILS = ['admin@example.org',]
DEFAULT_FROM_EMAIL = 'OpenData Team <info@example.org>'
EMAIL_SUBJECT_PREFIX = '[OpenData.org] '
SERVER_EMAIL = 'OpenData Team <info@example.org>'

MANAGERS = (
     ('OpenData Team', 'info@example.org'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'catalog',                      # Or path to database file if using sqlite3.
        'USER': 'catalog',                      # Not used with sqlite3.
        'PASSWORD': 'passw0rd',                  # Not used with sqlite3.
        'HOST': '',                      # Set to 'localhost' for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

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
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
ADMIN_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'admin_media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

STATIC_DATA = os.path.join(os.path.dirname(__file__), 'static/')

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/hidden/static/admin_media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

### Package settings
ACCOUNT_ACTIVATION_DAYS = 7
TWITTER_TIMEOUT = 6000
THUMBNAIL_EXTENSION = 'png'
PAGINATION_DEFAULT_WINDOW = 2
###

COMMENTS_APP = 'OpenDataCatalog.comments'

AUTH_PROFILE_MODULE = 'opendata.odpuserprofile'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    "OpenDataCatalog.opendata.context_processors.get_current_path",
    "OpenDataCatalog.opendata.context_processors.get_settings",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_sorting.middleware.SortingMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'OpenDataCatalog.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'south',
    'OpenDataCatalog.opendata',
    'registration',
    'sorl.thumbnail',
    'pagination',
    'django_sorting',
    'djangoratings',
    'OpenDataCatalog.comments',
    'OpenDataCatalog.suggestions',
    'OpenDataCatalog.contest',
    'OpenDataCatalog.catalog',

)

# the hostname of the deployment
SITEHOST = None
# the port which the deployment runs on
SITEPORT = None

# pycsw configuration
CSW = {
    'metadata:main': {
        'identification_title': 'Open Data Catalog CSW',
        'identification_abstract': 'Open Data Catalog is an open data catalog based on Django, Python and PostgreSQL. It was originally developed for OpenDataPhilly.org, a portal that provides access to open data sets, applications, and APIs related to the Philadelphia region. The Open Data Catalog is a generalized version of the original source code with a simple skin. It is intended to display information and links to publicly available data in an easily searchable format. The code also includes options for data owners to submit data for consideration and for registered public users to nominate a type of data they would like to see openly available to the public.',
        'identification_keywords': 'odc,Open Data Catalog,catalog,discovery',
        'identification_keywords_type': 'theme',
        'identification_fees': 'None',
        'identification_accessconstraints': 'None',
        'provider_name': ADMINS[0][0],
        'provider_url': 'https://github.com/azavea/Open-Data-Catalog',
        'contact_name': ADMINS[0][0],
        'contact_position': ADMINS[0][0],
        'contact_address': 'TBA',
        'contact_city': 'City',
        'contact_stateorprovince': 'State',
        'contact_postalcode': '12345',
        'contact_country': 'United States of America',
        'contact_phone': '+01-xxx-xxx-xxxx',
        'contact_fax': '+01-xxx-xxx-xxxx',
        'contact_email': ADMINS[0][1],
        'contact_url': 'https://github.com/azavea/Open-Data-Catalog/',
        'contact_hours': '0800h - 1600h EST',
        'contact_instructions': 'During hours of service.  Off on weekends.',
        'contact_role': 'pointOfContact',
    },
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except Exception:
    pass

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    LOCAL_STATICFILE_DIR,
    os.path.abspath(os.path.join(os.path.dirname(__file__),
                                 'opendata/static')),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    LOCAL_TEMPLATE_DIR,
    os.path.join(os.path.dirname(__file__), 'templates')
)

LOGIN_URL = SITE_ROOT + "/accounts/login/"
