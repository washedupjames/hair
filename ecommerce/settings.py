import environ
import os

env = environ.Env()
environ.Env.read_env()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['hairgrow.onrender.com', '*']

CSRF_TRUSTED_ORIGINS =  ['https://hairgrow.onrender.com/']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'store', # Django app

    'cart', # Django app

    'account', # Django app

    'payment', # Django app

    'mathfilters',

    'crispy_forms', # Crispy forms

    'django_countries',

    'storages',

]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

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
                'store.views.categories',

                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

'''
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

# Add this line to set the STATIC_ROOT
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'static/media'



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

HOST_EMAIL = 'parkerman23@gmail.com'

EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Allow Paypal popups
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'





AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID') # - env('SECRET_KEY') Enter your AWS ACCESS KEY ID HERE
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY') # - Enter your AWS SECRET ACCESS KEY HERE


# Amazon S3 Integration

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME') # - Enter your S3 bucket name HERE

# Django 4.2 > Storage configuration for S3

STORAGES = {
    
    # Media file (image) management

    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
    
    # CSS and JS file management

    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        
    },
    
}


AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_FILE_OVERWRITE = False





# RDS (Database) configuration settings:
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': env('DB_NAME'), # Enter your Database name HERE

        'USER': env('DBUSER'), # Enter your Database username HERE

        'PASSWORD': env('DBPASSWORD'), # Enter your Database password HERE

        'HOST': env('DB_HOST'),

        'PORT': '5432',
    }
}



