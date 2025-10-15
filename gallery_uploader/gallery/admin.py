from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['title']
    readonly_fields = ['uploaded_at']