from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Image
from .forms import ImageUploadForm

class ImageCreateView(CreateView):
    model = Image
    form_class = ImageUploadForm
    template_name = 'gallery/upload.html'
    success_url = reverse_lazy('image_list')

    def form_valid(self, form):

        return super().form_valid(form)

class ImageListView(ListView):
    model = Image
    template_name = 'gallery/image_list.html'
    context_object_name = 'images'
    ordering = ['-uploaded_at']  
    paginate_by = 12 