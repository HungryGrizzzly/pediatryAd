from .base import *

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR+"/../../../data/", 'db.sqlite3'),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR+"/../../../", 'media')