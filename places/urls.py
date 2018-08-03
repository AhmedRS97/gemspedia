# from django.conf.urls import url
from .views import PlaceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'places', PlaceViewSet, base_name='place')

urlpatterns = router.urls
# [
#     url(r'^$', PlaceList.as_view(), name='PlaceList'),
#     url(r'^(?P<pk>[\d]+)/$', PlaceDetail.as_view(), name='PlaceDetail'),
#     url(r'^(?P<pk>[\d]+)/delete/$', PlaceDelete.as_view(), name='PlaceDelete'),
#     url(r'^(?P<pk>[\d]+)/update/$', update_place, name='PlaceUpdate'),
#     url(r'^create/$', create_place, name='PlaceCreate'),
# ]
