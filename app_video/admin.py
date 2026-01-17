from django.contrib import admin

from app_video.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at", "updated_at")
    list_filter = ("category", "status", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("title", "description", "video_file", "thumbnail")}),
        ("Category & Status", {"fields": ("category", "status")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
