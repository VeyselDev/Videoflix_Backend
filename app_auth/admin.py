from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from app_auth.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_staff", "is_active", "last_login")
    list_filter = ("is_staff", "is_active", "is_superuser")
    readonly_fields = ("last_login", "created_at", "updated_at")
    search_fields = ("email", "username")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Timestamps", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )