import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-mm$5=7=^6srk=d%@g@$++umss0qmako9)d3t5)ko5)d-yz4*e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mailfinderdb',
        'USER': 'mailadmin',
        'PASSWORD': 'alakio12345',
        'HOST': 'localhost',
        'PORT': '',
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
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USE_TLS=True
# EMAIL_HOST_USER=os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASS')
EMAIL_HOST_USER = 'netrobeweb@gmail.com'
EMAIL_HOST_PASSWORD = 'wpcgtxfwmiqnlbwv'
# Custom user defined mail username
# DEFAULT_FROM_EMAIL = 'info@xcrowme.com'
DEFAULT_FROM_EMAIL = 'mailfinder@gmail.com'
DEFAULT_COMPANY_EMAIL = 'netrobeweb@gmail.com'

# DEA KEYS
# DEC_LOADER = "Scraper.utils.custom_email_domain_loader"

# GOOGLE SEARCH KEYS
GOOGLE_SEARCH_API_KEY = "AIzaSyCgbUr7E_QlweVanuX5u4OU65YCc9MhVYM"
GOOGLE_CSE_ID = "de1155bc82c628903"

# Email Validator Class Conf
STOP_STMP_CHECK = True
VALIDATION_TIME = 30

# SCRAPING CONF
SCRAPING_TIME = 30
