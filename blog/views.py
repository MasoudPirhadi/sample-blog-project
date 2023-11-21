from django.shortcuts import render, get_object_or_404
from datetime import date

from article_module.models import Article

all_posts = [
    {
        'slug': 'learning-django',
        'title': 'django courses',
        'author': 'Masoud Pirhadi',
        'image': 'django.png',
        'date': date(2023, 4, 6),
        'short_description': 'this is django project with Masoud',
        'content': """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit.
         A asperiores aspernatur aut autem consequuntur
            deleniti dedent dicta dolore error
            exercitationem expedita iusto labore laboriosam minus natus nesciunt non optio, placeat quis ratione
            reiciendis repudiandae rerum soluta suscipit tempora ut voluptatem.
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. A asperiores aspernatur aut autem consequuntur
            deleniti dedent dicta dolore error
            exercitationem expedita iusto labore laboriosam minus natus nesciunt non optio, placeat quis ratione
            reiciendis repudiandae rerum soluta suscipit tempora ut voluptatem.
            Lorem ipsum dolor sit amet, consectetur adipisicing elit.
             A asperiores aspernatur aut autem consequuntur
            deleniti dedent dicta dolore error
            exercitationem expedita iusto labore laboriosam minus natus nesciunt non optio, placeat quis ratione
            reiciendis repudiandae rerum soluta suscipit tempora ut voluptatem.
        """
    },
    {
        'slug': 'learning-python',
        'title': 'python courses',
        'author': 'Masoud Pirhadi',
        'image': 'python.png',
        'date': date(2022, 11, 10),
        'short_description': 'this is python project with Masoud',
        'content': """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. A asperiores aspernatur aut autem consequuntur
            deleniti dedent dicta dolore error
            exercitationem expedita iusto labore laboriosam minus natus nesciunt non optio, placeat quis ratione
            reiciendis repudiandae rerum soluta suscipit tempora ut voluptatem.
        """
    },
    {
        'slug': 'learning-machine-learning',
        'title': 'ml courses',
        'author': 'Masoud Pirhadi',
        'image': 'ml.png',
        'date': date(2022, 12, 1),
        'short_description': 'this is ml project with Masoud',
        'content': """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. A asperiores aspernatur aut autem consequuntur
            deleniti dedent dicta dolore error
            exercitationem expedita iusto labore laboriosam minus natus nesciunt non optio, placeat quis ratione
            reiciendis repudiandae rerum soluta suscipit tempora ut voluptatem.
        """
    },
]


# Create your views here.

def get_date(post):
    return post['date']


def index(request):
    # sorted_posts = sorted(all_posts, key=get_date)
    # latest_posts = sorted_posts[-2:]
    # return render(request, 'blog/index.html', {'end_post': latest_posts})
    articles = Article.objects.filter(is_active=True)
    return render(request, 'blog/index.html', {'articles': articles})


def posts(request):
    articles = Article.objects.filter(is_active=True)
    return render(request, 'blog/all-posts.html', {'articles': articles})


def single_post(request, slug):
    articles = get_object_or_404(Article, slug=slug, is_active=True)
    return render(request, 'blog/post-detail.html', {'article': articles})

