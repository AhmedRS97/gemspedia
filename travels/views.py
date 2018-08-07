# from datetime import datetime, timedelta
# from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.cache import caches
from rest_framework import viewsets

from .models import Travel

from .serializers import TravelSerializer


db_cache = caches['db']


# Create your views here.
class TravelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Travel instances.
    """
    serializer_class = TravelSerializer
    queryset = Travel.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action not in ['retrieve', 'list']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in self.permission_classes]

# class TravelList(ListView):
#     model = Travel
#     template_name = 'travels/list_travels.html'
#     context_object_name = 'travels'
#     queryset = Travel.objects.filter(start__date__gte=datetime.now().date())
#
#     def get_context_data(self, **kwargs):
#         context = super(TravelList, self).get_context_data(**kwargs)
#         context.update({
#             'popular_authors': db_cache.get('popular_authors'),
#             'popular_articles': db_cache.get('popular_articles'),
#             'popular_events': db_cache.get('popular_events')
#         })
#         return context
#
#
# class TravelDetail(DetailView):
#     model = Travel
#     template_name = 'travels/detail_travel.html'
#     context_object_name = 'travel'
#
#     def get_context_data(self, **kwargs):
#         context = super(TravelDetail, self).get_context_data(**kwargs)
#         context.update({
#             'popular_authors': db_cache.get('popular_authors'),
#             'popular_articles': db_cache.get('popular_articles'),
#             'popular_events': db_cache.get('popular_events')
#         })
#         return context
