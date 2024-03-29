from django.db import models

from common.miscellaneous import get_file_path
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
# from multimedia.models import Image, Video
# from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(max_length=1024)
    address = models.CharField(max_length=255)
    cover_img = models.ImageField(upload_to=get_file_path(file_dir='places-cover-imgs/'))
    # events = models.ForeignKey('events.Event', related_name='location', blank=True)
    # travels = models.ForeignKey('travels.Travel', related_name='location', blank=True, null=True)
    created = models.DateTimeField(_('Time Created'), auto_now_add=True, editable=True, null=True)  # add current date.
    updated = models.DateTimeField(_('Time Updated'), auto_now=True, editable=True)  # update date.
    # images = GenericRelation(Image, related_query_name='places')
    # videos = GenericRelation(Video, related_query_name='places')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class PlaceImage(models.Model):
    image = models.ImageField(upload_to=get_file_path('imgs/places/'))
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')


class PlaceVideo(models.Model):
    video = models.FileField(upload_to=get_file_path('vids/places/'))
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='videos')
