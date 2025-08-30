from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from webapp.models import Photo
from webapp.forms import PhotoForm
from django.http import Http404

class PhotoListView(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'
    context_object_name = 'photos'
    paginate_by = 5
    def get_queryset(self):
        return Photo.objects.filter(is_public=True).order_by('-created_at')


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'
    context_object_name = 'photo'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_public and (not self.request.user.is_authenticated or self.request.user != obj.author):
            raise Http404
        return obj


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect('webapp:photo_list')


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    def test_func(self):
        photo = self.get_object()
        return photo.author == self.request.user


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("album_detail", kwargs={"pk": self.object.album.pk})