import os
from django.core.management.utils import get_random_secret_key

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', '1433'),
        'OPTIONS': {
            'driver': os.environ.get('DATABASE_OPTIONS_DRIVER', 'ODBC Driver 18 for SQL Server'),
        },
    }
}

# URLs configuration
ROOT_URLCONF = 'pret_bancaire.pret_bancaire.urls'
