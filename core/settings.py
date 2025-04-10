"""
Django settings for oduma_platform project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

import dj_database_url

import sys
print(f"Python version: {sys.version}")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bu-u^(x&*qllbv-@16pwnweq$^j5qv#gwb$@3t2@rnvv2hu5o-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0', 'connect.onrender.com', 'connect-j2bu.onrender.com', 'connect-ihni.onrender.com']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    # 'docs',
    # 'oduma_platform.templates',
    # 'tailwind',

    # 'theme',
    # 'django_browser_reload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'core.urls'

INTERNAL_IPS = [
    "127.0.0.1",
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR,'core','docs/')],
        # 'DIRS': [os.path.join(BASE_DIR,'core','templates/','docs/')],

        'DIRS': [os.path.join(BASE_DIR,'docs')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.app.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


from dotenv import load_dotenv

load_dotenv() 

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default="").split(",")

DATABASES = {
    
    # postgresql://austin:WPnHyrtaq6mPjwTummEEtz4EMQtN7PON@dpg-cvj2kl6uk2gs73b0vkb0-a.oregon-postgres.render.com/odumaconnectdb
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

        # 'ENGINE': 'django.db.backends.postgresql',  # Change accordingly
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default="localhost"),
        'PORT': config('DB_PORT', default="5432"),

         
    }
    #     'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'odumaconnectdb',
    #     'USER': 'austin',
    #     'PASSWORD': 'WPnHyrtaq6mPjwTummEEtz4EMQtN7PON',
    #     # 'HOST': 'localhost',
    #     'HOST': 'odumaconnect.onrender.com',
    #     # 'HOST': 'postgresql://austin:WPnHyrtaq6mPjwTummEEtz4EMQtN7PON@dpg-cvj2kl6uk2gs73b0vkb0-a/odumaconnectdb',
    #     'PORT': '5432',
    # }
}
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'yourdbname',
       
#     }
# }


STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIR = [os.path.join( BASE_DIR,'docs')]
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

##whitenoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'core.CustomUser'

# TAILWIND_APP_NAME = 'theme'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'



 # Use an app password if using Gmail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"