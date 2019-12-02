# -*- coding: utf-8 -*-
"""
Settings for tests
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    # core django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # third party
    "sorl.thumbnail",
    "private_storage",
    "phonenumber_field",
    "crispy_forms",
    "rest_framework",
    "small_small_hr",
    "django_tables2",
    "django_filters",
    "vega_admin",
    # custom
    "tiny_erp.apps.locations",
    "tiny_erp.apps.products",
    "tiny_erp.apps.purchases",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "tiny_erp",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_L10N = True
USE_TZ = True

SECRET_KEY = "i love oov"

PRIVATE_STORAGE_ROOT = "/tmp/"
MEDIA_ROOT = "/tmp/"
PRIVATE_STORAGE_AUTH_FUNCTION = "private_storage.permissions.allow_staff"
DEBUG = True

SITE_ID = 1

# vega settings
CRISPY_TEMPLATE_PACK = "bootstrap3"
VEGA_TEMPLATE = "badmin"

ROOT_URLCONF = "tests.crud"

STATIC_URL = "/static/"

# try and load local_settings if present
try:
    # pylint: disable=wildcard-import
    # pylint: disable=unused-wildcard-import
    from .local_settings import *  # noqa
except ImportError:
    pass
