# from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import caches
from rest_framework import viewsets  # , status

from .models import User
from .serializers import UserSerializer

db_cache = caches['db']


class UserViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing User instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['get'], detail=False)
    def popular_authors(self, request):
        serializer = self.get_serializer(db_cache.get('popular_authors'), many=True)
        return Response(serializer.data)
