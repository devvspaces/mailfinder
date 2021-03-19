import os
import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Read the configuration files and load them to the required fields
CONFIG_LOCATION = os.path.join(BASE_DIR, 'MailFinder/config.json')
# CONFIG_LOCATION = 'config.json'
with open(CONFIG_LOCATION, 'r') as f:
    config = json.loads(f.read())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['GENERAL'][0]['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['GENERAL'][0]['DEBUG']

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Account',
    'Mobile',
    'Scraper',
    'Payment',
]

AUTH_USER_MODEL = 'Account.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MailFinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'MailFinder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


if config['GENERAL'][0]['CUSTOM_DB']:
    DATABASES = {
        'default': {
            'ENGINE': config['GENERAL'][0]['ENGINE'],
            'NAME': config['GENERAL'][0]['NAME'],
            'USER': config['GENERAL'][0]['USER'],
            'PASSWORD': config['GENERAL'][0]['PASSWORD'],
            'HOST': config['GENERAL'][0]['HOST'],
            'PORT': config['GENERAL'][0]['PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS= [
    os.path.join(BASE_DIR, 'assets/')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


#Emails settings
EMAIL_BACKEND=config['EMAIL_CONF'][0]['EMAIL_BACKEND']
EMAIL_HOST=config['EMAIL_CONF'][0]['EMAIL_HOST']
EMAIL_PORT=config['EMAIL_CONF'][0]['EMAIL_PORT']
EMAIL_USE_TLS=config['EMAIL_CONF'][0]['EMAIL_USE_TLS']
EMAIL_HOST_USER = config['EMAIL_CONF'][0]['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = config['EMAIL_CONF'][0]['EMAIL_HOST_PASSWORD']
# Custom user defined mail username
DEFAULT_FROM_EMAIL = config['EMAIL_CONF'][0]['DEFAULT_FROM_EMAIL']
DEFAULT_COMPANY_EMAIL = config['EMAIL_CONF'][0]['DEFAULT_COMPANY_EMAIL']

# DEA KEYS
# DEC_LOADER = "Scraper.utils.custom_email_domain_loader"

# GOOGLE SEARCH KEYS
GOOGLE_SEARCH_API_KEY = config['GOOGLE_SEARCH_KEYS'][0]['GOOGLE_SEARCH_API_KEY']
GOOGLE_CSE_ID = config['GOOGLE_SEARCH_KEYS'][0]['GOOGLE_CSE_ID']

# Email Validator Class Conf
STOP_STMP_CHECK = config['EMAIL_VERIFICATION_CONF'][0]['STOP_STMP_CHECK']
VALIDATION_TIME = config['EMAIL_VERIFICATION_CONF'][0]['VALIDATION_TIME']
# SCRAPING CONF
SCRAPING_TIME = config['EMAIL_VERIFICATION_CONF'][0]['SCRAPING_TIME']


# USEFUL FIXED HUNTER.IO API REQUIREMENTS
EMAIL_TYPE = (
    ('1', 'personal',),
    ('2', 'generic',),
)
SENIOR_TYPE = (
    ('1', 'junior',),
    ('2', 'senior',),
    ('3', 'executive',),
)


# HUNTER.IO API KEY
HUNTER_API_KEY = config['HUNTER_API'][0]['HUNTER_API_KEY']
