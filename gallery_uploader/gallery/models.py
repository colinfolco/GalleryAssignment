from django.db import models
from django.contrib.auth.models import User
import os
from uuid import uuid4

def image_upload_path(instance, filename):
    """Generate unique path for uploaded images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('gallery', filename)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Image(models.Model):
    image = models.ImageField(upload_to=image_upload_path)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True) 

    def __str__(self):
        return self.title or f"Image {self.id}"

    def save(self, *args, **kwargs):
        if not self.title and self.image:
            self.title = os.path.splitext(self.image.name)[0]
        super().save(*args, **kwargs)

class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100, default='Anonymous')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40)  

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.image.title}"