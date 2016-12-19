"""
Django settings for suggestdataset project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dotenv
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read environment variables
dotenv.read_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', '3ss+te5koy+))l6$r)=hw6d1-#r%kodx(9tbh#2h95lcs^v!5q')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(' ')

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'crispy_forms',
    'import_export',
    'el_pagination',
    'django_comments',
    'widget_tweaks',
    'phonenumber_field',
    'datasets',
    'mrejesho',
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'suggestdataset.urls'

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
                'suggestdataset.context_processors.site'
            ],
        },
    },
]

WSGI_APPLICATION = 'suggestdataset.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=int(os.environ.get('DATABASE_CONN_MAX_AGE', 600))),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql_psycopg2'),
            'NAME': os.environ.get('DATABASE_NAME', 'suggestdataset'),
            'USER': os.environ.get('DATABASE_USER', 'suggestdataset'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'suggestdataset'),
            'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
            'PORT': os.environ.get('DATABASE_PORT', '5432'),
            'CONN_MAX_AGE': int(os.environ.get('DATABASE_CONN_MAX_AGE', 600))
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'sw')

ugettext = lambda s: s
LANGUAGES = (
    ('sw', ugettext('Kiswahili')),
    ('en', ugettext('English')),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

TIME_ZONE = os.environ.get('TIME_ZONE', 'Africa/Dar_es_Salaam')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATIC_URL = os.environ.get('STATIC_URL', '/static/')

STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static_root'))

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

# STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE', 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage')

# Site

SITE_ID = 1

SITE_NAME = os.environ.get('SITE_NAME', ugettext('Open Data Suggestions'))

ADMIN_SITE_HEADER = os.environ.get('ADMIN_SITE_HEADER', ugettext('Open Data Suggestions'))

ADMIN_INDEX_TITLE = os.environ.get('ADMIN_INDEX_TITLE', ugettext('Management'))

# Auth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = os.environ.get('LOGIN_REDIRECT_URL', '/')

# Forms

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Comments

COMMENTS_HIDE_REMOVED = True

# extras
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

