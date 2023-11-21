from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='articles_list'),
    path('cat/<str:category>', views.ArticleView.as_view(), name='articles_by_category_list'),
    path('<pk>/', views.ArticleDetailView.as_view(), name='articles_detail'),
    path('preview/<pk>/', views.ArticlePreview.as_view(), name='articles_preview'),
    path('add-article-comment', views.add_article_comment, name='add_article_comment'),
    path('search', views.SearchArticles.as_view(), name='search'),
]
