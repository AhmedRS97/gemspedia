# from django.conf.urls import url
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = router.urls
