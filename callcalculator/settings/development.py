from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ty31hsk@#473=4pkej$4)&@e1mq)e)!c%3@t)(m934*zzxhty'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dev.sqlite3'),
    }
}
