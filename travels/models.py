from django.db import models
from places.models import Place
from accounts.models import User

from django.utils.translation import ugettext_lazy as _
from common.miscellaneous import get_file_path
from ckeditor.fields import RichTextField
# from multimedia.models import Image, Video
# from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Travel(models.Model):
    users = models.ManyToManyField(User, related_name='travels', blank=True)
    title = models.CharField(_('title'), max_length=255, db_index=True)
    description = RichTextField(max_length=1024)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, db_index=True)
    has_offer = models.BooleanField(default=False)
    offer = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)
    limit = models.PositiveIntegerField()
    location = models.ForeignKey(Place, related_name='travels')
    created = models.DateTimeField(_('Time Created'), auto_now_add=True)  # add current date.
    # images = GenericRelation(Image, related_query_name='travels')
    # videos = GenericRelation(Video, related_query_name='travels')

    class Meta:
        index_together = ['start', 'end']

    def __str__(self):
        return self.title

    def get_price_difference(self):
        return self.price - self.offer

    @property
    def duration(self):
        if (self.end - self.start).days <= 1:
            return 1
        return (self.end - self.start).days

    @classmethod
    def get_upcoming_travels(cls, start, end):
        return cls.objects.filter(start__date__gte=start, end__date__lte=end).order_by('start')


class TravelImage(models.Model):
    image = models.ImageField(upload_to=get_file_path('imgs/travels/'))
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='images')


class TravelVideo(models.Model):
    video = models.FileField(upload_to=get_file_path('vids/travels/'))
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='videos')
