from django.db import models
from places.models import Place
from accounts.models import User

from common.miscellaneous import get_file_path
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
# from django.contrib.contenttypes.fields import GenericRelation
# from multimedia.models import Image, Video
from django.conf import settings

import stripe


# Create your models here.
class Event(models.Model):
    users = models.ManyToManyField(User, related_name='events', blank=True)
    location = models.ForeignKey(Place, related_name='events')
    title = models.CharField(_('title'), max_length=255)
    description = RichTextField(max_length=2048)
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, blank=True, null=True)
    limit = models.PositiveIntegerField()
    available_seats = models.PositiveSmallIntegerField()
    created = models.DateTimeField(_('Time Created'), auto_now_add=True)  # add current date.
    # images = GenericRelation(Image, related_query_name='events')
    # videos = GenericRelation(Video, related_query_name='events')

    class Meta:
        index_together = ['start', 'end']
        ordering = ['start']

    def __str__(self):
        return self.title

    @property
    def duration(self):
        if (self.end - self.start).days <= 1:
            return 1
        return (self.end - self.start).days

    @property
    def price_in_cents(self):
        return int(str(self.price).replace('.', ''))

    @classmethod
    def get_upcoming_events(cls, start, end):
        return cls.objects.filter(start__date__gte=start, end__date__lte=end).order_by('start')

    def charge(self, token, description, user, currency='usd', tickets=1, capture=True):
        """
        charges the user, add him to the event and create event reservation if the event have a price.
        :param token: Str
        :param description: Str
        :param user: QuerySet object
        :param currency: Str
        :param tickets: Integer
        :param capture: Boolean
        :return: Boolean
        """
        if capture:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                charge = stripe.Charge.create(
                    amount=self.price_in_cents*tickets, currency=currency, source=token, description=description
                )
                reservation = self.reservations.create(
                    user=user, event=self, tickets=tickets, charge_id=charge['id'], paid=True
                )
                return reservation
            except stripe.error.CardError as e:
                print('there was an error charging the user.')
                return False
        else:
            try:
                charge = stripe.Charge.create(
                    amount=self.price_in_cents*tickets, currency=currency, source=token, description=description,
                    capture=False
                )
                reservation = self.reservations.create(
                    user=user, event=self, tickets=tickets, charge_id=charge['id']
                )
                return reservation
            except stripe.error.CardError as e:
                print('there was an error charging the user.')
                return False


class EventImage(models.Model):
    image = models.ImageField(upload_to=get_file_path('imgs/events/'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')


class EventVideo(models.Model):
    video = models.FileField(upload_to=get_file_path('vids/events/'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='videos')



