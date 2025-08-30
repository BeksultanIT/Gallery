from django.contrib import admin
from .models import Album, Photo




@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at', 'author')
    search_fields = ('title', 'description', 'author__username')



@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'author', 'album', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at', 'author')
    search_fields = ('caption', 'author__username')