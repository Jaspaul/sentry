# This file is just Python, with a touch of Django which means
# you can inherit and tweak settings to your hearts content.
import os.path

import dj_database_url
from sentry.conf.server import *

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {'default': dj_database_url.config()}

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = True

# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
# General #
###########

# The administrative email for this installation.
# Note: This will be reported back to getsentry.com as the point of contact. See
# the beacon documentation for more information. This **must** be a string.

SENTRY_ADMIN_EMAIL = os.environ.get('SENTRY_ADMIN_EMAIL', '')

# Instruct Sentry that this install intends to be run by a single organization
# and thus various UI optimizations should be enabled.
SENTRY_SINGLE_ORGANIZATION = True

# Should Sentry allow users to create new accounts?
SENTRY_FEATURES['auth:register'] = False

#########
# Redis #
#########

# Generic Redis configuration used as defaults for various things including:
# Buffers, Quotas, TSDB

redis_url = urlparse.urlparse(os.environ['REDIS_URL'])
SENTRY_REDIS_OPTIONS = {
    'hosts': {
        0: {
            'host': redis_url.hostname,
            'port': redis_url.port,
            'password': redis_url.password,
            'db': 0,
        }
    }
}

#########
# Cache #
#########

# If you wish to use memcached, install the dependencies and adjust the config
# as shown:
#
#   pip install python-memcached
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': ['127.0.0.1:11211'],
#     }
# }
#
# SENTRY_CACHE = 'sentry.cache.django.DjangoCache'

SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

#########
# Queue #
#########

# See https://docs.getsentry.com/on-premise/server/queue/ for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

CELERY_ALWAYS_EAGER = False
BROKER_URL = os.environ['REDIS_URL'] + '/0'

###############
# Rate Limits #
###############

# Rate limits apply to notification handlers and are enforced per-project
# automatically.

SENTRY_RATELIMITER = 'sentry.ratelimits.redis.RedisRateLimiter'

##################
# Update Buffers #
##################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'

##########
# Quotas #
##########

# Quotas allow you to rate limit individual projects or the Sentry install as
# a whole.

SENTRY_QUOTAS = 'sentry.quotas.redis.RedisQuota'

########
# TSDB #
########

# The TSDB is used for building charts as well as making things like per-rate
# alerts possible.

SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'

################
# File storage #
################

# Any Django storage backend is compatible with Sentry. For more solutions see
# the django-storages package: https://django-storages.readthedocs.org/en/latest/

SENTRY_FILESTORE = 'django.core.files.storage.FileSystemStorage'
SENTRY_FILESTORE_OPTIONS = {
    'location': '/tmp/sentry-files',
}

##############
# Web Server #
##############

# You MUST configure the absolute URI root for Sentry:
SENTRY_URL_PREFIX = os.environ['SENTRY_URL_PREFIX']

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = int(os.environ['PORT'])
SENTRY_WEB_OPTIONS = {
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    'worker_class': 'gevent',
    'workers': 3,
}

ALLOWED_HOSTS = ['jaspaul-sentry.herokuapp.com', 'sentry.notimedeveloper.com']

###############
# Mail Server #
###############

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if 'SENDGRID_USERNAME' in os.environ:
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
elif 'MANDRILL_USERNAME' in os.environ:
    EMAIL_HOST = 'smtp.mandrillapp.com'
    EMAIL_HOST_USER = os.environ['MANDRILL_USERNAME']
    EMAIL_HOST_PASSWORD = os.environ['MANDRILL_APIKEY']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# The email address to send on behalf of
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'root@localhost')

# If you're using mailgun for inbound mail, set your API key and configure a
# route to forward to /api/hooks/mailgun/inbound/
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', '')

############
# Security #
############

INSTALLED_APPS += ('djangosecure',)
MIDDLEWARE_CLASSES += ('djangosecure.middleware.SecurityMiddleware',)

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# header and uncomment the following settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Whether to use HTTPOnly flag on the session cookie. If this is set to `True`,
# client-side JavaScript will not to be able to access the session cookie.
SESSION_COOKIE_HTTPONLY = True

# Whether to use a secure cookie for the session cookie.  If this is set to
# `True`, the cookie will be marked as "secure," which means browsers may
# ensure that the cookie is only sent under an HTTPS connection.
SESSION_COOKIE_SECURE = True

# If set to `True`, causes `SecurityMiddleware` to set the
# `X-Content-Type-Options: nosniff` header on all responses that do not already
# have that header.
SECURE_CONTENT_TYPE_NOSNIFF = True

# If set to `True`, causes `SecurityMiddleware` to set the
# `X-XSS-Protection: 1; mode=block` header on all responses that do not already
# have that header.
SECURE_BROWSER_XSS_FILTER = True

# If set to `True`, causes `SecurityMiddleware` to set the `X-Frame-Options:
# DENY` header on all responses that do not already have that header
SECURE_FRAME_DENY = True

# If set to a non-zero integer value, causes `SecurityMiddleware` to set the
# HTTP Strict Transport Security header on all responses that do not already
# have that header.
SECURE_HSTS_SECONDS = 31536000

# If `True`, causes `SecurityMiddleware` to add the ``includeSubDomains`` tag
# to the HTTP Strict Transport Security header.
#
# Has no effect unless ``SECURE_HSTS_SECONDS`` is set to a non-zero value.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# If set to True, causes `SecurityMiddleware` to redirect all non-HTTPS
# requests to HTTPS
SECURE_SSL_REDIRECT = True

##########
# Bcrypt #
##########

INSTALLED_APPS += ('django_bcrypt',)

# Enables bcrypt password migration on a ``check_password()`` call.
#
# The hash is also migrated when ``BCRYPT_ROUNDS`` changes.
BCRYPT_MIGRATE = True

###############
# Social Auth #
###############

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')

FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_API_SECRET = os.environ.get('FACEBOOK_API_SECRET')

GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')

GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_API_SECRET = os.environ.get('GITHUB_API_SECRET')
GITHUB_ORGANIZATION = os.environ.get('GITHUB_ORGANIZATION')
GITHUB_EXTENDED_PERMISSIONS = ['repo']

BITBUCKET_CONSUMER_KEY = os.environ.get('BITBUCKET_CONSUMER_KEY')
BITBUCKET_CONSUMER_SECRET = os.environ.get('BITBUCKET_CONSUMER_SECRET')

########
# etc. #
########

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = os.environ['SECRET_KEY']
