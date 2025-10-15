from django.urls import path
from .views import ImageCreateView, ImageListView

urlpatterns = [
    path('', ImageListView.as_view(), name='image_list'),
    path('upload/', ImageCreateView.as_view(), name='image_upload'),
]