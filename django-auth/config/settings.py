"""
Django settings for Django project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!c=on9r3kw*++-#(6i=blt=0uy7)lh_h$lo7edj$cy_8euchaf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # Django app's
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.auth',

    # Third part app's
    'rest_framework',
    'corsheaders',
    'django_s3_storage',

    # Developed app's
    'app.authentication',
]

MIDDLEWARE = [
    # Third part
    'corsheaders.middleware.CorsMiddleware',
    
    # Django
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = 'authentication.Account'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'  # edited

TIME_ZONE = 'America/Sao_Paulo'  # edited

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

MEDIA_URL = config('MEDIA_URL', default="/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = config('STATIC_URL', default="/static/")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

if not DEBUG:
    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
    STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'

    AWS_S3_KEY_PREFIX = 'media/'
    AWS_S3_KEY_PREFIX_STATIC = 'static/'

    AWS_S3_BUCKET_NAME = config('S3_BUCKET_NAME')
    AWS_S3_BUCKET_NAME_STATIC = config('S3_BUCKET_NAME')

    MEDIA_URL = f'{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/'
    STATIC_URL = f'{AWS_S3_BUCKET_NAME_STATIC}.s3.amazonaws.com/'

    # Make public
    AWS_S3_BUCKET_AUTH = False
    AWS_S3_MAX_AGE_SECONDS = 60 * 60  # 1 hour caching

    # OR...if you create a fancy custom domain for your static files use:
    #AWS_S3_PUBLIC_URL_STATIC = "https://static.zappaguide.com/"

# Django rest configuration 
# https://www.django-rest-framework.org/api-guide/settings/
# https://github.com/davesque/django-rest-framework-simplejwt

REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
    )
}

# Django Cors Configuration
# https://github.com/adamchainz/django-cors-headers

CORS_ORIGIN_ALLOW_ALL = True

# “Common” middleware
# https://docs.djangoproject.com/en/2.2/ref/middleware/#django.middleware.common.CommonMiddleware
APPEND_SLASH = False

# Django Logging
# https://docs.djangoproject.com/en/2.2/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'gateway': {
            'format': '[%(asctime)s] [%(levelname)s] Auth - %(message)s',
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './logs/requests.log',
            'formatter': 'gateway',
        },
    },
    'loggers': {
        'gateway': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}