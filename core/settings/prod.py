from core.settings.base import *
from core.utils.env_helper_utils import get_list_env


DEBUG = False

ALLOWED_HOSTS = get_list_env('ALLOWED_HOSTS', [])
CSRF_TRUSTED_ORIGINS = get_list_env('CSRF_TRUSTED_ORIGINS', [])
CORS_ALLOWED_ORIGINS = get_list_env('CORS_ALLOWED_ORIGINS', [])
CORS_ALLOW_CREDENTIALS = True

COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

STATIC_ROOT = BASE_DIR / 'static'