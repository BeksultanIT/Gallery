from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import  DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from webapp.models import Photo, Album
from webapp.forms import AlbumForm
from django.http import Http404





class AlbumDetailView(DetailView):
    model = Album
    template_name = 'album/album_detail.html'
    context_object_name = 'album'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_public and (not self.request.user.is_authenticated or self.request.user != obj.author):
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        photos = self.object.photos.filter(is_public=True).order_by('-created_at')
        paginator = Paginator(photos, 9)
        page = self.request.GET.get('page')
        ctx['photos_page'] = paginator.get_page(page)
        return ctx


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'form.html'

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect('webapp:album_detail', pk=self.object.pk)


class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'form.html'

    def test_func(self):
        album = self.get_object()
        return album.author == self.request.user

    def form_valid(self, form):
        old = self.get_object()
        was_public = old.is_public
        album = form.save(commit=False)
        album.save()
        if was_public and not album.is_public:
            album.photos.update(is_public=False)
        return redirect('webapp:album_detail', pk=album.pk)


class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    success_url = reverse_lazy("album_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)




class TogglePhotoFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        if not photo.can_be_favorited():
            return redirect(photo.get_absolute_url() if hasattr(photo, 'get_absolute_url') else 'gallery:photo_detail', pk=pk)
        if request.user in photo.favorited_by.all():
            photo.favorited_by.remove(request.user)
        else:
            photo.favorited_by.add(request.user)
        return redirect(request.META.get('HTTP_REFERER', reverse('gallery:photo_detail', args=[pk])))

