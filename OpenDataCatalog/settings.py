import os
# Django settings for opendata project.

SITE_ROOT = ""
RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""

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

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/projects/OpenDataCatalog/opendata/static",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'insecure'

### Package settings
ACCOUNT_ACTIVATION_DAYS = 7
TWITTER_USER = None
TWITTER_TIMEOUT = 6000
THUMBNAIL_EXTENSION = 'png'
PAGINATION_DEFAULT_WINDOW = 2
###

LOGIN_URL = SITE_ROOT + "/accounts/login/"

COMMENTS_APP = 'comments'

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
    "django.core.context_processors.request",
    
    "opendata.context_processors.get_current_path",
    "opendata.context_processors.get_settings",
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

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates')
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
#    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'south',
    'opendata',
    'registration',
    'sorl.thumbnail',
    'pagination',
    'django_sorting',
    'djangoratings',
    'comments',
    'suggestions',
    'contest',
    'csw',
    'owslib',
    
)

# Set this to the location of the pycsw config file
CSW_CONFIG = None

MD_CORE_MODEL = {
    'typename': 'pycsw:CoreMetadata',
    'outputschema': 'http://pycsw.org/metadata',
    'mappings': {
        'pycsw:Identifier': 'id',
        'pycsw:Typename': 'atype',
        'pycsw:Schema': 'name',
        'pycsw:InsertDate': 'release_date',
        'pycsw:XML': 'description',
        'pycsw:AnyText': 'description',
        'pycsw:BoundingBox': 'bbox',
        'pycsw:Links': 'name',
        'pycsw:Keywords': 'short_description',
        'pycsw:Title': 'name',
        'pycsw:Contributor': 'created_by_id',
        'pycsw:Source': 'created_by_id',
        'pycsw:Language': 'metadata_notes',
        'pycsw:Creator': 'created_by_id',
        'pycsw:Type': 'name',
        'pycsw:Modified': 'created',
        'pycsw:AccessConstraints': 'name',
        'pycsw:Abstract': 'name',
        'pycsw:Relation': 'name',
        'pycsw:Date': 'created',
        'pycsw:Publisher': 'created_by_id',
        'pycsw:Format': 'name',
        # 'pycsw:MdSource': 'mdsource',
        # 'pycsw:KeywordType': 'keywordstype',
        # 'pycsw:CRS': 'crs',
        # 'pycsw:AlternateTitle': 'title_alternate',
        # 'pycsw:RevisionDate': 'date_revision',
        # 'pycsw:CreationDate': 'date_creation',
        # 'pycsw:PublicationDate': 'date_publication',
        # 'pycsw:OrganizationName': 'organization',
        # 'pycsw:SecurityConstraints': 'securityconstraints',
        # 'pycsw:ParentIdentifier': 'parentidentifier',
        # 'pycsw:TopicCategory': 'topicategory',
        # 'pycsw:ResourceLanguage': 'resourcelanguage',
        # 'pycsw:GeographicDescriptionCode': 'geodescode',
        # 'pycsw:Denominator': 'denominator',
        # 'pycsw:DistanceValue': 'distancevalue',
        # 'pycsw:DistanceUOM': 'distanceuom',
        # 'pycsw:TempExtent_begin': 'time_begin',
        # 'pycsw:TempExtent_end': 'time_end',
        # 'pycsw:ServiceType': 'servicetype',
        # 'pycsw:ServiceTypeVersion': 'servicetypeversion',
        # 'pycsw:Operation': 'operation',
        # 'pycsw:CouplingType': 'couplingtype',
        # 'pycsw:OperatesOn': 'operateson',
        # 'pycsw:OperatesOnIdentifier': 'operatesonidentifier',
        # 'pycsw:OperatesOnName': 'operatesoname',
        # 'pycsw:Degree': 'degree',
        # 'pycsw:OtherConstraints': 'otherconstraints',
        # 'pycsw:Classification': 'classification',
        # 'pycsw:ConditionApplyingToAccessAndUse': 'conditionapplyingtoaccessanduse',
        # 'pycsw:Lineage': 'lineage',
        # 'pycsw:ResponsiblePartyRole': 'responsiblepartyrole',
        # 'pycsw:SpecificationTitle': 'specificationtitle',
        # 'pycsw:SpecificationDate': 'specificationdate',
        # 'pycsw:SpecificationDateType': 'specificationdatetype',
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
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
