from .common import *
import django_heroku

# Activate Django-Heroku.
django_heroku.settings(locals())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cnomvl^^xh_xsc)ke-hfkj&j5hfa%gjc^-aobdkv*0v_(e!k##'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'caioaraujo-callcalculator.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'prod.sqlite3'),
    }
}
