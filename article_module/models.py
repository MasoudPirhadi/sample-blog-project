from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField
from comment.models import Comment
from account.models import User
from django.db import models
from star_ratings.models import Rating


# Create your models here.

class ArticleManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آی پی')

    def __str__(self):
        return self.ip_address


class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_CHOICES = [
        ('d', 'پیش نویس'),  # draft
        ('p', 'منتشر شده'),  # publish
        ('i', 'درحال بررسی'),  # investigation
        ('b', 'برگشت داده شده'),  # back
    ]
    title = models.CharField(max_length=200, verbose_name=_('Article Title'), default='0')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name=_('Title in URL'),  default='0')
    image = models.ImageField(upload_to='images/articles', verbose_name=_('image'))
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name=_('Text'), default='0')
    selected_categories = models.ManyToManyField(ArticleCategory, verbose_name=_('Categories'))
    is_active = models.CharField(max_length=100, verbose_name='وضعیت', choices=STATUS_CHOICES)
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', null=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت', editable=False)
    hits = models.ManyToManyField(IpAddress, verbose_name='بازدید ها', related_name='hits', through='ArticleHits')
    ratings = GenericRelation(Rating, related_query_name='articles')
    comments = GenericRelation(Comment)

    def active_categories(self):  # az in tarigh category haye active ro migirim.
        return self.selected_categories.filter(is_active=True)

    def category_list(self):  # baraye in ast ke category besoorate list hast ke az list miarim biroon.
        return '، '.join([category.title for category in self.active_categories()])

    def get_absolute_url(self):
        return reverse('articles_detail', kwargs={'pk': self.pk})

    category_list.short_description = 'دسته بندی'

    class Meta:
        ordering = ['-create_date']
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComment', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='نظر والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن نظر')

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقاله'

    def __str__(self):
        return str(self.user)


class ArticleHits(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقالات')
    ip_address = models.ForeignKey(IpAddress, on_delete=models.CASCADE, verbose_name='آی پی')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
