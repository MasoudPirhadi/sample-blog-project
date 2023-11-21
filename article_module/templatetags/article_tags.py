from datetime import timedelta, datetime

from django import template
from django.db.models import Count, Q, Max

from article_module.models import Article

register = template.Library()


@register.inclusion_tag('article_module/includes/more_views.html')
def sidebar_article():
    last_month = datetime.today() - timedelta(days=30)
    return {
        'more_view_article': Article.objects.filter(is_active='p').annotate(
            count=Count('hits', filter=Q(articlehits__create_date__gt=last_month))
        ).order_by('-count', '-create_date')[:5],

        'hot_article': Article.objects.filter(is_active='p').annotate(
            count=Count('comments', filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=7))
        ).order_by('-count', '-create_date')[:5],

        'rating_article': Article.objects.filter(is_active='p', create_date__gt=last_month).annotate(
            max_rating=Max('ratings')).order_by('-max_rating', '-create_date')[:5],
    }
