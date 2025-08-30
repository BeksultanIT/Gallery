from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Album, Photo
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(CreateView):
    model = User
    template_name = "register.html"
    fields = ['username', 'first_name', 'last_name', 'password']


    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('account:profile', kwargs={'user_id': self.object.id})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('account:profile', user_id=user.id)
        else:
            return render(request, "login.html", {"error": "Неверный логин или пароль"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    context_object_name = "profile_user"
    login_url = '/account/login/'

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs["user_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()

        public_albums = Album.objects.filter(author=profile_user, is_public=True)
        public_photos = Photo.objects.filter(author=profile_user, album__isnull=True, is_public=True)

        private_albums = []
        private_photos = []
        favorites = None

        if self.request.user == profile_user:
            private_albums = Album.objects.filter(author=profile_user, is_public=False)
            private_photos = Photo.objects.filter(author=profile_user, album__isnull=True, is_public=False)

        context.update({
            "public_albums": public_albums,
            "public_photos": public_photos,
            "private_albums": private_albums,
            "private_photos": private_photos,
            "favorites": favorites,
        })
        return context