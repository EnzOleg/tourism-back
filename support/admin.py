from django.contrib import admin
from .models import SupportRequest


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "status",
        "created_at"
    )
    list_filter = (
        "status",
        "created_at"
    )
    search_fields = (
        "name",
        "phone",
        "message"
    )
    list_editable = (
        "status",
    )