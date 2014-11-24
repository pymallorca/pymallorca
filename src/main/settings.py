# -*- coding: utf-8 -*-

import os

from configurations import Settings
from apconf.mixins import CachesMixin, DatabasesMixin, PathsMixin, LogsMixin
from apconf.mixins import SecurityMixin, DebugMixin, CompressMixin

from apconf import Options

opts = Options()


class Base(CachesMixin, DatabasesMixin, PathsMixin, LogsMixin, SecurityMixin,
           DebugMixin, CompressMixin, Settings):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'apconf',
        'raven.contrib.django.raven_compat',
        'captcha',
        'compressor',
        # 'crispy_forms',
        # 'django_tables2',
        # 'django_filters',

        'landing',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.request',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.debug',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
    )

    ROOT_URLCONF = 'main.urls'

    WSGI_APPLICATION = 'main.wsgi.application'

    LANGUAGES = (
        ('ca', 'Català'),
        ('es', 'Castellano'),
    )
    LANGUAGE_CODE = 'ca'

    gettext = lambda s: s

    TIME_ZONE = 'Europe/Madrid'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    APP_SLUG = opts.get('APP_SLUG', '')
    TEMPLATE_DIRS = ('templates', )

    # CRISPY_TEMPLATE_PACK = 'bootstrap3'

    # Django toolbar
    INTERNAL_IPS = ['127.0.0.1']
    LOGIN_URL = '/login'
    LOGIN_REDIRECT_URL = '/'

    SITE_ID = 1

    # Captcha
    RECAPTCHA_PUBLIC_KEY = opts.get("RECAPTCHA_PUBLIC_KEY",
                                    "6Ld9r-cSAAAAAN5UTgUFF5G2U31AmltZJTYwRX11")
    RECAPTCHA_PRIVATE_KEY = opts.get("RECAPTCHA_PRIVATE_KEY",
                                     "6Ld9r-cSAAAAAE_ijhjnXtX8rFtlKj0Xrp2VNaOd")

    RECAPTCHA_USE_SSL = True