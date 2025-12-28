from django.contrib import admin

from app_auth.models import CustomUser


admin.site.register(CustomUser)