"""
Django settings for {{cookiecutter.project_name}} project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd65i_7it8eaq8_ba7$&kx_nd%gukr0nx-znsnk%d2%$b()$9sc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party apps
    'django_filters',
{%- if cookiecutter.channels == 'yes' %}
    'channels',
{%- endif %}
{%- if cookiecutter.graphql == 'yes' %}
    'graphene_django',
{%- endif %}
{%- if cookiecutter.drf == 'yes' %}
    'rest_framework',
{%- endif %}
    # My apps
    'accounts.apps.AccountsConfig',
]

if DEBUG:
    INSTALLED_APPS += [
        'django_extensions',
        'debug_toolbar',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('CACHE_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "django_cache",
    },
}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/{{cookiecutter.project_name}}/static'

{%- if cookiecutter.drf == 'yes' %}
# Rest framework
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'PAGE_SIZE': 20,  # Max number of results returned from a list API call
}
{%- endif %}

{%- if cookiecutter.channels == 'yes' %}
# Django channels
ASGI_APPLICATION = 'config.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('{{cookiecutter.project_name}}-redis', 6379)],
        },
    },
}
{%- endif %}

# CELERY
CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:{port}/{vhost}/'.format(
    user=os.environ.get('RABBIT_USER'),
    password=os.environ.get('RABBIT_PASS'),
    host=os.environ.get('RABBIT_HOST'),
    port=os.environ.get('RABBIT_PORT'),
    vhost=os.environ.get('RABBIT_ENV_VHOST', ''),
)
CELERY_RESULT_BACKEND = os.environ.get('')
BROKER_HEARTBEAT = '?heartbeat=30'
CELERY_BROKER_URL += BROKER_HEARTBEAT

# Redis
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_HOST')

# Celery configuration

# configure queues, currently we have only one
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)

# Sensible settings for celery
# CELERY_TASK_ALWAYS_EAGER = False
# CELERY_TASK_ACKS_LATE = True
# CELERY_TASK_PUBLISH_RETRY = True
# CELERY_WORKER_DISABLE_RATE_LIMITS = False

# By default we will ignore result
# If you want to see results and try out tasks interactively, change it to False
# Or change this setting on tasks level
# CELERY_TASK_IGNORE_RESULT = True
# CELERY_RESULT_EXPIRES = 600

# Don't use pickle as serializer, json is much safer
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']

# CELERY_WORKER_HIJACK_ROOT_LOGGER = False
# CELERY_WORKER_PREFETCH_MULTIPLIER = 1
# CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000

{%- if cookiecutter.graphql == 'yes' %}
GRAPHENE = {
    'SCHEMA': 'config.schema.schema', # Where your Graphene schema lives
    'MIDDLEWARE': []
}
if DEBUG:
    GRAPHENE['MIDDLEWARE'].append('graphene_django.debug.DjangoDebugMiddleware')

{%- endif %}

