"""
Django settings for cloud project.

Generated by 'django-admin startproject' using Django 1.8.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import abspath, basename, dirname, join, normpath
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DJANGO_ROOT = dirname(dirname(abspath(__file__)))
# SITE_ROOT = dirname(DJANGO_ROOT)
# SITE_NAME = basename(DJANGO_ROOT)

# sys.path.append(SITE_ROOT)
# sys.path.append(normpath(join(DJANGO_ROOT, 'apps')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'emxygq=ck7a@tfno-5sk$f2@ct^6y^_d8t&%@*&53=#h-2d$t5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.tenant',
    'apps.landlord',
    'apps.fb_bot',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'cloud.urls'

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

WSGI_APPLICATION = 'cloud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': os.environ.get("DB_DEFAULT_NAME", 'ichef_dev'),
    #     'USER': os.environ.get("DB_DEFAULT_USER", 'admin'),
    #     'PASSWORD': os.environ.get("DB_DEFAULT_PASSWORD", 'ichefitco'),
    #     'HOST': os.environ.get("DB_DEFAULT_HOST", "127.0.0.1"),
    #     'PORT': os.environ.get("DB_DEFAULT_PORT", '3306'),
    # },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# iCHEF LOGIN AUTH CONFIGURATION
AUTH_USER_MODEL = 'landlord.LandlordUser'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'apps.landlord.auth_backend.AuthBackend',
)

SERVER_URL = os.environ.get("SERVER_URL")
PAGE_ACCESS_TOKEN = "EAAR5rDguPHEBALZCFu5JI26SpM5bhYInto3YjcmQ6NyyOCXXWZBNuz4gAgi9Ba6x7F5yHvRv35sLCOXYaZBV7xALRZCszHu01ZCtOPBEfKUxpkyVRAWG8IIabEY4DZAZCVTzE1cZAtW9EiimfsGYzDz9DDym2pm8A3IGRd0BYWSyVgZDZD"
