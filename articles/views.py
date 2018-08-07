# from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.permissions import IsAuthor
from django.core.cache import caches
from rest_framework import status, viewsets
from django.conf import settings
import redis


from .models import Article
from .serializers import ArticleSerializer
# from accounts.models import User

db_cache = caches['db']
# connect to redis
r = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Article instances.
    """
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action not in ['retrieve', 'list', 'popular']:
            self.permission_classes = [IsAuthenticated, IsAuthor]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # increment Author ranking by 1
        r.zincrby('author_ranking', instance.user.id, 1)
        # increment article ranking by 1
        r.zincrby('article_ranking', instance.id, 1)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def popular(self, request):
        serializer = self.get_serializer(db_cache.get('popular_articles'), many=True)
        return Response(serializer.data)


# class ArticleList(ListView):
#     model = Article
#     template_name = 'articles/list_articles.html'
#     context_object_name = 'articles'
#
#     def get_context_data(self, **kwargs):
#         context = super(ArticleList, self).get_context_data(**kwargs)
#         context.update({
#             'popular_authors': db_cache.get('popular_authors'),
#             'popular_articles': db_cache.get('popular_articles'),
#             'popular_events': db_cache.get('popular_events')
#         })
#         return context
#
#
# class ArticleDetail(DetailView):
#     model = Article
#     template_name = 'articles/detail_article.html'
#     context_object_name = 'article'
#
#     def get_context_data(self, **kwargs):
#         context = super(ArticleDetail, self).get_context_data(**kwargs)
#         context.update({
#             # increment total image views by 1
#             'total_views': r.incr('article:{}:views'.format(self.object.id)),
#             'popular_authors': db_cache.get('popular_authors'),
#             'popular_articles': db_cache.get('popular_articles'),
#             'popular_events': db_cache.get('popular_events')
#
#         })
#         # increment Author ranking by 1
#         r.zincrby('author_ranking', self.object.user.id, 1)
#         # increment article ranking by 1
#         r.zincrby('article_ranking', self.object.id, 1)
#         return context
#
#
# @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Authors').exists() or u.is_superuser),
#                   name='dispatch')
# class ArticleDelete(LoginRequiredMixin, DeleteView):
#     model = Article
#     success_url = reverse_lazy('articles:ArticleList')
#
#
# @login_required()
# @user_passes_test(lambda u: u.groups.filter(name='Authors').exists() or u.is_superuser)
# def create_article(request):
#     form = CreateArticleForm(request.POST or None, request.FILES or None)
#     form2 = CreateVideoForm(request.POST or None, request.FILES or None)
#     if form.is_valid() and form2.is_valid():
#         article = form.save(commit=False)
#         article.user = User.objects.get(pk=request.user.pk)
#         article.slug = slugify(article.title)
#         article.save()
#         return HttpResponseRedirect("/articles/{article.pk}/update/")
#     #                                                           context_instance=RequestContext(request))
#     return render(request, 'articles/create_article.html', {'form': form, 'form2': form2})
#
#
# @login_required()
# @user_passes_test(lambda u: u.groups.filter(name='Authors').exists() or u.is_superuser)
# def update_article(request, pk):
#     article = get_object_or_404(Article, id=pk)
#     form = CreateArticleForm(request.POST or None, request.FILES or None, instance=article)
#     # vid_form = CreateVideoForm(request.POST or None, request.FILES or None)
#     if form.is_valid(): # vid_form.is_valid()
#         if form.has_changed():
#             form.save()
#             return HttpResponseRedirect("/articles/{pk}/update")
#         # print(form1.errors, form2.errors)
#     return render(request, 'articles/update_article.html',
#                   {'form': form})


