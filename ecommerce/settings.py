import os
from pathlib import Path
import environ
env = environ.Env()

import environ
import os
from dotenv import load_dotenv

load_dotenv()  # Assuming your .env file is in the right place
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
SANDBOX_PAYPAL_CLIENT_ID = os.getenv('SANDBOX_PAYPAL_CLIENT_ID')
env = environ.Env()
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    env.read_env(dotenv_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # Adjusted for correct path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'tees-naturals.online',
    'www.tees-naturals.online', 
    '*'
]

CSRF_TRUSTED_ORIGINS = [
    'https://www.tees-naturals.online',
    'https://tees-naturals.online',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',  # Django app
    'cart',   # Django app
    'account',  # Django app
    'payment',  # Django app
    'mathfilters',
    'crispy_forms',  # Crispy forms
    'django_countries',
    'storages',
]

# To un-block PayPal popups - NB!
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

# Crispy forms
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
                'store.views.categories',  # Updated
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'




# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'static/media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = 'True'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')  # Enter your GMAIL address
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # Enter your app password 
HOST_EMAIL = env('EMAIL_HOST_USER')

# Database

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),  
        'USER': env('DBUSER'),   
        'PASSWORD': env('DBPASSWORD'),  
        'HOST': env('DB_HOST'),  
        'PORT': '5432',
    }
}



# AWS configuration
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')  
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')  
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')  

# Django 4.2 > Storage configuration for S3
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False

"""
