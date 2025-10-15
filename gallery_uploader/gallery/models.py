from django.db import models
import os
from uuid import uuid4

def image_upload_path(instance, filename):
    """Generate unique path for uploaded images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('gallery', filename)

class Image(models.Model):
    image = models.ImageField(upload_to=image_upload_path)
    title = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image {self.id}"

    def save(self, *args, **kwargs):
        if not self.title and self.image:
            self.title = os.path.splitext(self.image.name)[0]
        super().save(*args, **kwargs)