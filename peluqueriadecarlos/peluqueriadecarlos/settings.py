"""
Django settings for peluqueriadecarlos project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from dotenv import load_dotenv
from pathlib import Path
import os
import dj_database_url

import pymysql
pymysql.install_as_MySQLdb()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!^w3g@%71f*$&k$nx@&*a2n_6_$n%strhn40+4iq-==9wctd-t"

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ["*"]

# ALLOWED_HOSTS = ["peluqueriadecarlos.vercel.app", ".vercel.app", "127.0.0.1"]


# ALLOWED_HOSTS = []
# RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
# if RENDER_EXTERNAL_HOSTNAME:
#     ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    "agenda",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
     'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "peluqueriadecarlos.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "peluqueriadecarlos.wsgi.application"

WSGI_APPLICATION = "peluqueriadecarlos.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'peluqueria',
         'USER': 'barberia',
         'PASSWORD': 'q.JJb,rke,utw+4-d119',
         'HOST': 'localhost',
         'PORT': '3306',
         'OPTIONS': {
             'charset': 'utf8mb4',
         }
     }
 }

#barberia
# load_dotenv()

# DATABASES = {
#      'default': dj_database_url.config(
#          default="mysql://root:@127.0.0.1:3306/peluqueria"
#     )
#  }




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = (
     os.path.join(BASE_DIR, 'static'),
 )



STATIC_URL = '/static/'
STATICFILES_DIRS = [
     os.path.join(BASE_DIR, 'static')
 ]







# Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración específica para PWA
PWA_APP_NAME = 'peluqueriadecarlos'
PWA_APP_SHORT_NAME = 'agenda'
PWA_APP_ICONS = [
    {
        'src': '/static/agenda/carlosimagen.ico ',
        'sizes': '192x192',
        'type': 'image/png'
    },
    {
        'src': '/static/agenda/carlosimagen.ico ',
        'sizes': '512x512',
        'type': 'image/png'
    }
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"





# Configuración de sesiones
SESSION_COOKIE_AGE = 86400  # Duración predeterminada de la sesión en segundos (1 día)
SESSION_SAVE_EVERY_REQUEST = True  # Actualiza la cookie de sesión en cada solicitud

# Si quieres usar cookies de sesión basadas en el navegador sin utilizar la base de datos
# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Configuraciones de seguridad para las cookies
SESSION_COOKIE_SECURE = True  # Solo enviar cookies a través de HTTPS (recomendado en producción)
SESSION_COOKIE_HTTPONLY = True  # Evitar acceso a las cookies desde JavaScript
LOGIN_REDIRECT_URL = "adminis"