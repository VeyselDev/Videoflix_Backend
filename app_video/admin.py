from django.contrib import admin

from app_video.models.video import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at", "updated_at")
    list_filter = ("category", "status", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at",)
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("title", "description", "file", "thumbnail")}),
        ("Category", {"fields": ("category",)}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return self.readonly_fields
        return self.readonly_fields + ("file",)