# from django.conf.urls import url
from .views import ArticleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, base_name='article')

urlpatterns = router.urls
# [
#     url(r'^$', ArticleList.as_view(), name='ArticleList'),
#     url(r'^create/$', create_article, name='ArticleCreate'),
#     url(r'^(?P<slug>[\w-]+)/$', ArticleDetail.as_view(), name='ArticleDetail'),
#     url(r'^(?P<pk>[\d]+)/delete/$', ArticleDelete.as_view(), name='ArticleDelete'),
#     url(r'^(?P<pk>[\d]+)/update/$', update_article, name='ArticleUpdate'),
# ]

