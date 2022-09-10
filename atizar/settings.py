import os
from pathlib import Path

envvar_bool = lambda envvar, default: os.environ.get(envvar, default).lower() in ('true', '1', 't')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = envvar_bool('DEBUG', 'False')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1|localhost').split('|')

INSTALLED_APPS = [
    'abastece.apps.AbasteceConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'usuarios',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'atizar.urls'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


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

WSGI_APPLICATION = 'atizar.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['MYSQL_DATABASE'],
        'USER': os.environ['MYSQL_USER'],
        'PASSWORD': os.environ['MYSQL_PASSWORD'],
        'HOST': os.environ['MYSQL_HOST'],
        'PORT': os.environ['MYSQL_PORT'],
    }
}

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
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/usuarios/login/'
LOGOUT_URL = '/usuarios/logout/'
AUTH_USER_MODEL = 'usuarios.User'
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Catamarca'
USE_I18N = False
USE_L10N = False
USE_TZ = True


SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
ADMINS = [
    (os.environ.get('ADMIN_NAME'), os.environ.get('ADMIN_MAIL')),
]
MANAGERS = ADMINS

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 465))
EMAIL_USE_SSL = envvar_bool('EMAIL_USE_SSL', 'True')


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.'
                   'FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
    }
}