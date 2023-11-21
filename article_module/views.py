from datetime import datetime, timedelta

from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import activate
from django.views import View
from django.views.generic import ListView, DetailView

from account.mixins import AuthorAccessMixin
from article_module.models import Article, ArticleCategory, ArticleComment


# Create your views here.


# class ArticleView(View):
#     def get(self, request):
#         articles = Article.objects.filter(is_active=True)
#         context = {'articles': articles}
#         return render(request, 'article_module/article_page.html', context)

class ArticleView(ListView):
    template_name = 'article_module/article_page.html'
    context_object_name = 'Articles'
    model = Article
    paginate_by = 2

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active='p')
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


def site_lang(request):
    activate(request.GET.get('lang'))
    return redirect(request.GET.get('next'))


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'
    context_object_name = 'article_detail'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active='p')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article: Article = kwargs.get('object')
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by(
            '-create_date').prefetch_related('articlecomment_set')

        # for ip address view
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        context['article'] = article
        return context


class ArticlePreview(AuthorAccessMixin, DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'
    context_object_name = 'article_detail'
    queryset = Article.objects.all()


def article_categories_component(request: HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,
                                                                                                     parent_id=None)
    context = {'main_categories': article_main_categories}
    return render(request, 'article_module/component/article_categories_component.html', context)


def add_article_comment(request):
    if request.user.is_authenticated:
        article_comment = request.GET.get('article_comment')
        article_id = request.GET.get('article_id')
        parent_id = request.GET.get('parent_id')
        new_comment = ArticleComment(article_id=article_id, user_id=request.user.id, text=article_comment,
                                     parent_id=parent_id)
        new_comment.save()
        comments = ArticleComment.objects.filter(article_id=article_id, parent=None).order_by(
            '-create_date').prefetch_related('articlecomment_set')
        comments_count = ArticleComment.objects.filter(article_id=article_id).count()
        context = {
            'comments': comments,
            'comments_count': comments_count
        }
        return render(request, 'article_module/includes/article_comments_partial.html', context)
    return HttpResponse('response')


class SearchArticles(ListView):
    template_name = 'article_module/article_search.html'
    paginate_by = 2

    def get_queryset(self):
        search = self.request.GET.get('q')
        article = Article.objects.filter(Q(title__icontains=search) | Q(text__icontains=search))
        return article

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['search'] = self.request.GET.get('q')
        return context
