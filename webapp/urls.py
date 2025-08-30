from django.urls import path
from webapp.views import PhotoListView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView, PhotoDetailView, TogglePhotoFavoriteView, AlbumDetailView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', PhotoListView.as_view(), name='photo_list'),
    path('photo/add/', PhotoCreateView.as_view(), name='photo_add'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/<int:pk>/edit/', PhotoUpdateView.as_view(), name='photo_edit'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('photo/<int:pk>/favorite-toggle/', TogglePhotoFavoriteView.as_view(), name='photo_fav_toggle'),


    path('album/add/', AlbumCreateView.as_view(), name='album_add'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('album/<int:pk>/edit/', AlbumUpdateView.as_view(), name='album_edit'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
]
