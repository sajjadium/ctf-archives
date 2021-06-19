from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-p*sk-&$*0qb^j3@_b07a38kzus7d^&)-elk6rmoh1&__6yv^bf'
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = []
MIDDLEWARE = [
    'cache.cache_middleware.SimpleMiddleware',
]
ROOT_URLCONF = 'cache.urls'
TEMPLATES = []
WSGI_APPLICATION = 'cache.wsgi.application'
DATABASES = {}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
