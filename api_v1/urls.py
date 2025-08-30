from django.urls import path
from api_v1.views import add_photo_to_favorites, remove_photo_from_favorites, add_album_to_favorites, remove_album_from_favorites

app_name = 'api_v1'

urlpatterns = [
    path('photo/<int:photo_id>/favorites/add/', add_photo_to_favorites, name='add_photo_favorite'),
    path('photo/<int:photo_id>/favorites/remove/', remove_photo_from_favorites, name='remove_photo_favorite'),
    path('album/<int:album_id>/favorites/add/', add_album_to_favorites, name='add_album_favorite'),
    path('album/<int:album_id>/favorites/remove/', remove_album_from_favorites, name='remove_album_favorite'),
]