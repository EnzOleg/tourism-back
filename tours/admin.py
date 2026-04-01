from django.contrib import admin
from .models import Tour, TourImage

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1  
    fields = ('image', 'is_main', 'order')

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'country', 'price')
    search_fields = ('title', 'city')
    inlines = [TourImageInline]