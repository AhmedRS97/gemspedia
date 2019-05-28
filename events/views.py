# from datetime import datetime
# from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.core.cache import caches

from .models import Event, EventImage, EventVideo

from .serializers import ReadEventSerializer, WriteEventSerializer, ImageSerializer, VideoSerializer
# from rest_framework.serializers import PrimaryKeyRelatedField, HyperlinkedRelatedField

db_cache = caches['db']


# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Event instances.
    """
    serializer_class = ReadEventSerializer
    queryset = Event.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action not in ['retrieve', 'list', 'popular']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            self.serializer_class = WriteEventSerializer
        return super(EventViewSet, self).get_serializer_class()

    def get_serializer_context(self):
        context = super(EventViewSet, self).get_serializer_context()
        context['images'] = self.request.data.pop('images', [])
        context['videos'] = self.request.data.pop('videos', [])
        return context

    @action(methods=['get'], detail=False)
    def popular(self, request):
        serializer = self.get_serializer(db_cache.get('popular_events'), many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def join(self, request, pk=None):
        event = self.get_object()
        has_reservation = event.reservations.filter(user=request.user, event=event).exists()
        tickets = int(request.data.get('tickets', 1))
        if not event.price and not has_reservation:
            event.users.add(request.user)
            event.reservations.create(user=request.user, event=event, tickets=tickets)
            event.available_seats -= tickets
            event.save()
            return Response({'status': 'user joined the event.'})
        elif event.price and not has_reservation:
            description = "resereved {tickets} tickets for {request.user.username}"
            charged = event.charge(request.data['stripeToken'], description, request.user, tickets=tickets)
            if charged:
                event.users.add(request.user)
                event.available_seats -= tickets
                event.save()
                return Response({'status': 'user joined the event.'})
            return Response(
                {'status': 'error charging the user, please try again.'}, status=status.HTTP_400_BAD_REQUEST
            )
        elif has_reservation:
            return Response({
                'not_permitted': 'action not permitted, you already made a reservation.'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'bad_request': 'there is unknown error happened.'}, status=status.HTTP_400_BAD_REQUEST)
        # return Response()


class EventImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = EventImage.objects.all()


class EventVideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = EventVideo.objects.all()


# class EventList(ListView):
#     model = Event
#     queryset = Event.objects.filter(start__date__gte=datetime.now().date())
#     template_name = 'events/list_events.html'
#     context_object_name = 'events'
#
#     def get_context_data(self, **kwargs):
#         context = super(EventList, self).get_context_data(**kwargs)
#         context.update({
#             'popular_authors': db_cache.get('popular_authors'),
#             'popular_articles': db_cache.get('popular_articles'),
#             'popular_events': db_cache.get('popular_events')
#         })
#         return context
#
#
# class EventDetail(DetailView):
#     model = Event
#     template_name = 'events/detail_event.html'
#     context_object_name = 'event'
#
#     def get_context_data(self, **kwargs):
#         context = super(EventDetail, self).get_context_data(**kwargs)
#         context.update({
#             'popular_authors': db_cache.get('popular_authors'),
#             'popular_articles': db_cache.get('popular_articles'),
#             'popular_events': db_cache.get('popular_events')
#         })
#         return context
