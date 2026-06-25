from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*h39n8!ae3p8w7$9iz&*ik3r0y$h!-ryh1=(9uxrss_2k*%4ki'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clients',
    'rooms',
    'reservations',
    'services',
    'image_uploader_widget',
    'contacts',
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

ROOT_URLCONF = 'Hotels.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Hotels.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'HotelDB',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'clients.Client'

AUTHENTICATION_BACKENDS = [
    'clients.backends.ClientAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'clients:login'
LOGIN_REDIRECT_URL = 'clients:profile'
LOGOUT_REDIRECT_URL = 'clients:login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'partygamestop007@gmail.com'
EMAIL_HOST_PASSWORD = 'vwoaopxwsgwcyfeu'
DEFAULT_FROM_EMAIL = 'partygamestop007@gmail.com'
ADMIN_EMAIL = 'partygamestop007@gmail.com'




import logging

logging.getLogger('django.contrib.admin').disabled = True
logging.getLogger('django.contrib.auth').disabled = True
logging.getLogger('django.db.backends').disabled = True
logging.getLogger('django.request').disabled = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'django.contrib.admin': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'django.contrib.auth': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['null'],
            'level': 'CRITICAL',
            'propagate': False,
        },
    },
}
