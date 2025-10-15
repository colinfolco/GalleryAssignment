from django.contrib import admin
from .models import Image, Tag, Comment

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'session_key']
    list_filter = ['uploaded_at', 'tags']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at']
    filter_horizontal = ['tags']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'image', 'created_at', 'session_key']
    list_filter = ['created_at']
    search_fields = ['author', 'text']
    readonly_fields = ['created_at']