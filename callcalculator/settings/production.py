from .common import *
import django_heroku
import dj_database_url

# Activate Django-Heroku.
django_heroku.settings(locals())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('TOP_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'caioaraujo-callcalculator.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {'default': dj_database_url.config()}
