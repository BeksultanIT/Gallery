from django import forms
from .models import Photo, Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'is_public']

    def save(self, commit=True, user=None):
        album = super().save(commit=False)
        if user is not None and not album.pk:
            album.author = user
        if commit:
            album.save()
        return album


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'album', 'is_public']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if self.user is not None:
            self.fields['album'].queryset = Album.objects.filter(author=self.user)

    def clean(self):
        cleaned = super().clean()
        album = cleaned.get('album')
        is_public = cleaned.get('is_public')
        if album and not album.is_public and is_public:
            raise forms.ValidationError(
                "нельз сдеплать фотографию публичной если она находится в приватном альбоме"
            )
        return cleaned

    def save(self, commit=True, user=None):
        photo = super().save(commit=False)
        if user and not photo.pk:
            photo.author = user
        if photo.album and not photo.album.is_public:
            photo.is_public = False
        if commit:
            photo.save()
            self.save_m2m()
        return photo
