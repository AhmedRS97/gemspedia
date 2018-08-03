# from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from django.core.cache import caches
from rest_framework import viewsets

from .models import Place

from .serializers import PlaceSerializer
db_cache = caches['db']


# Create your views here.
class PlaceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Place instances.
    """
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action not in SAFE_METHODS:
            self.permission_classes += [IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class PlaceList(ListView):
#     model = Place
#     template_name = 'places/list_places.html'
#     context_object_name = 'places'
#
#     def get_context_data(self, **kwargs):
#         context = super(PlaceList, self).get_context_data(**kwargs)
#         context.update({
#             'popular_authors': db_cache.get('popular_authors'),
#             'popular_articles': db_cache.get('popular_articles'),
#             'popular_events': db_cache.get('popular_events')
#         })
#         return context
#
#
# class PlaceDetail(DetailView):
#     model = Place
#     template_name = 'places/detail_place.html'
#     context_object_name = 'place'
#
#     def get_context_data(self, **kwargs):
#         context = super(PlaceDetail, self).get_context_data(**kwargs)
#         context.update({
#             'popular_authors': db_cache.get('popular_authors'),
#             'popular_articles': db_cache.get('popular_articles'),
#             'popular_events': db_cache.get('popular_events')
#         })
#         return context
