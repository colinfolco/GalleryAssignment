from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Image, Comment, Tag
from .forms import ImageUploadForm, CommentForm

class ImageCreateView(CreateView):
    model = Image
    form_class = ImageUploadForm
    template_name = 'gallery/upload.html'
    success_url = reverse_lazy('image_list')

    def form_valid(self, form):
        if not self.request.session.session_key:
            self.request.session.create()
        form.instance.session_key = self.request.session.session_key
        
        response = super().form_valid(form)

        new_tags = form.cleaned_data.get('new_tags', '')
        existing_tags = form.cleaned_data.get('existing_tags', [])

        if existing_tags:
            self.object.tags.add(*existing_tags)

        if new_tags:
            tag_names = [name.strip() for name in new_tags.split(',') if name.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                self.object.tags.add(tag)
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        return context

class ImageListView(ListView):
    model = Image
    template_name = 'gallery/image_list.html'
    context_object_name = 'images'
    ordering = ['-uploaded_at']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
 
        tag_filter = self.request.GET.get('tag')
        if tag_filter:
            queryset = queryset.filter(tags__name=tag_filter)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get('tag')
        context['search_query'] = self.request.GET.get('search', '')

        if self.request.session.session_key:
            context['my_images'] = Image.objects.filter(
                session_key=self.request.session.session_key
            ).order_by('-uploaded_at')

        viewing_history = self.request.session.get('viewing_history', [])
        context['viewing_history'] = Image.objects.filter(
            id__in=viewing_history
        ).order_by('-uploaded_at')
        
        return context

class ImageDetailView(DetailView):
    model = Image
    template_name = 'gallery/image_detail.html'
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        if not self.request.session.session_key:
            self.request.session.create()
        
        viewing_history = self.request.session.get('viewing_history', [])
        image_id = str(self.object.id)

        if image_id in viewing_history:
            viewing_history.remove(image_id)
        viewing_history.insert(0, image_id)

        viewing_history = viewing_history[:10]
        self.request.session['viewing_history'] = viewing_history
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = self.object
            if not request.session.session_key:
                request.session.create()
            comment.session_key = request.session.session_key
            comment.save()
            return redirect('image_detail', pk=self.object.pk)
        
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.session.session_key == comment.session_key:
        image_pk = comment.image.pk
        comment.delete()
        return redirect('image_detail', pk=image_pk)
    
    return redirect('image_list')