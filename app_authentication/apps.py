from django.apps import AppConfig


class AppAuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_authentication'

    def ready(self):
        from .scheduler import schedule_delete_inactive_users
        schedule_delete_inactive_users()
