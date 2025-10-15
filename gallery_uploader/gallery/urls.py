from django.urls import path
from .views import ImageCreateView, ImageListView, ImageDetailView, delete_comment

urlpatterns = [
    path('', ImageListView.as_view(), name='image_list'),
    path('upload/', ImageCreateView.as_view(), name='image_upload'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='image_detail'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
]