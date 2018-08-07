# from django.conf.urls import url
from .views import EventViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet, base_name='event')

urlpatterns = router.urls

# [
#     url(r'^$', EventList.as_view(), name='EventList'),
#     url(r'^(?P<pk>[\d]+)/$', EventDetail.as_view(), name='EventDetail'),
#     url(r'^(?P<pk>[\d]+)/delete/$', EventDelete.as_view(), name='EventDelete'),
#     url(r'^(?P<pk>[\d]+)/update/$', update_event, name='EventUpdate'),
#     url(r'^create/$', create_event, name='EventCreate'),
# ]

