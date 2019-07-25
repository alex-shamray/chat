"""
Django settings for chat_project project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import logging
import os
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '*',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'channels',
    'debug_toolbar',
    'django_filters',
    'import_export',
    'mptt',
    'rest_framework',
    'reversion',
    'chat',
    'core',
    'customers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'chat_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'contacts.context_processors.contact_form',
            ],
        },
    },
]

# Default form rendering class.
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'chat_project.wsgi.application'
ASGI_APPLICATION = 'chat_project.routing.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'common_files', 'locale'),
]

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = os.getenv('STATIC_ROOT')

# URL that handles the static files served from STATIC_ROOT.
STATIC_URL = '/static/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.getenv('MEDIA_ROOT')

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'

# A list of locations of additional static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Cache
# https://docs.djangoproject.com/en/2.1/topics/cache/

# The cache backends to use.
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
    }
}


# Authentication
# https://docs.djangoproject.com/en/2.1/topics/auth/customizing/

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'customers.backends.CustomerBackend',
]

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/accounts/'

LOGOUT_REDIRECT_URL = '/'


# Logging
# https://docs.djangoproject.com/en/2.2/topics/logging/

# Custom logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


# Channel Layers
# https://channels.readthedocs.io/en/latest/topics/channel_layers.html

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}


# Settings for REST framework
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    # Base API policies
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'oauth.authentication.JSONWebTokenAuthentication',
    ),

    # Generic view behavior
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',

    # Pagination
    'PAGE_SIZE': 100,
}
if not DEBUG:
    REST_FRAMEWORK.update({
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
    })


# Sentry
# https://docs.sentry.io/platforms/python/django/

sentry_logging = LoggingIntegration(
    level=logging.INFO,         # Capture info and above as breadcrumbs
    event_level=logging.WARNING # Send errors as events
)
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN', 'https://9935b7dedee048f39e3df7adcdd390ea@sentry.io/211961'),
    integrations=[DjangoIntegration(), CeleryIntegration(), sentry_logging],
    send_default_pii=True,
)


# Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'chat_project.debug_toolbar.show_toolbar',
}


# Celery settings

CELERY_BROKER_URL = os.getenv('BROKER_URL')
CELERY_BEAT_SCHEDULE = {
    'debug-every-300-seconds': {
        'task': 'chat_project.celery.debug_task',
        'schedule': 300.0,
    },
}
