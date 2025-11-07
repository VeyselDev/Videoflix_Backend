from django.contrib import admin

from app_authentication.models import CustomUser


admin.site.register(CustomUser)