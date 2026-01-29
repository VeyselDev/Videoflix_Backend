from core.settings.base import *
from core.utils.env_helper_utils import get_list_env

DEBUG = True
ALLOWED_HOSTS = get_list_env('ALLOWED_HOSTS', ['localhost'])
CSRF_TRUSTED_ORIGINS = get_list_env('CSRF_TRUSTED_ORIGINS', [])
CORS_ALLOWED_ORIGINS = get_list_env('CORS_ALLOWED_ORIGINS', [])
CORS_ALLOW_CREDENTIALS = get_bool_env('CORS_ALLOW_CREDENTIALS', True)
COOKIE_SECURE = False
STATICFILES_DIRS = [BASE_DIR / 'static']