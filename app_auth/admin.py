from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from app_auth.models.custom_user import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin configuration for the CustomUser model.

    Extends Django's built-in UserAdmin to customize how users are displayed
    and managed in the admin interface.

    Features:
    - Custom list display and filtering options
    - Search by email and username
    - Read-only timestamp fields
    - Structured fieldsets for detail and creation views
    """
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