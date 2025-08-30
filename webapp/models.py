from django.db import models
from django.conf import settings




class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True) # необязательное
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, related_name='favorite_albums')


    def __str__(self):
        return f"{self.title} ({'Public' if self.is_public else 'Private'})"




class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='photos')
    album = models.ForeignKey(Album,null=True,blank=True,on_delete=models.CASCADE,related_name='photos')
    is_public = models.BooleanField(default=True)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='favorite_photos')


    def __str__(self):
        return f"{self.caption[:30]} — {self.author}"


    class Meta:
        ordering = ['-created_at']


    def can_be_favorited(self):
        return self.is_public


    @property
    def favorites_count(self):
        return self.favorited_by.count()