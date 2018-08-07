# from datetime import datetime
# from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.core.cache import caches

from .models import Event
# from accounts.models import User

from .serializers import EventSerializer

db_cache = caches['db']


# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Event instances.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action not in ['retrieve', 'list', 'popular']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in self.permission_classes]

    @action(methods=['get'], detail=False)
    def popular(self, request):
        serializer = self.get_serializer(db_cache.get('popular_events'), many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def join(self, request, pk=None):
        event = self.get_object()
        has_reservation = event.reservations.filter(user=request.user, event=event).exists()
        if not event.price and not has_reservation:
            event.users.add(request.user)
            event.save()
            event.reservations.create(user=request.user, event=event, tickets=request.data['tickets'])
            return Response({'status': 'user joined the event.'})
        elif event.price and not has_reservation:
            event.users.add(request.user)
            event.save()
            description = "resereved "
            event.charge(request.data['stripeToken'], description, request.user, tickets=request.data['tickets'])
            return Response({'not_permitted': 'action not permitted, you must make a payment.'},
                            status=status.HTTP_402_PAYMENT_REQUIRED)
        # return Response()

    # @action(methods=['post'], detail=True)
    # def pay(self, request, pk=None):
    #     event = self.get_object()
    #     if not event.price:
    #         return Response({'not_permitted': "action not permitted, this event doesn't have a price."},
    #                         status=status.HTTP_400_BAD_REQUEST)
            

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
