# from django.conf.urls import url
from .views import TravelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'travels', TravelViewSet, base_name='travel')

urlpatterns = router.urls

# [
#     url(r'^$', TravelList.as_view(), name='TravelList'),
#     url(r'^(?P<pk>[\d]+)/$', TravelDetail.as_view(), name='TravelDetail'),
#     url(r'^(?P<pk>[\d]+)/delete/$', TravelDelete.as_view(), name='TravelDelete'),
#     url(r'^(?P<pk>[\d]+)/update/$', update_travel, name='TravelUpdate'),
#     url(r'^create/$', create_travel, name='TravelCreate'),
# ]

