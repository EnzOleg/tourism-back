from django.contrib import admin
from .models import Tour, TourImage


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "country", "city", "price", "duration_days")
    list_filter = ("country", "city")
    search_fields = ("title", "country", "city")
    filter_horizontal = ("hotels",)
    inlines = [TourImageInline]


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ("id", "tour", "is_main", "order")