from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from article_module.models import Article


class FieldsMixin():
    """
    zamani ke az in mixin ha estefade konim moteghayer fields dar view pak mishe va azinja mikhone.
    """

    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            'title',
            'slug',
            'image',
            'short_description',
            'text',
            'selected_categories',
            'is_active',
            'is_special',
        ]
        if request.user.is_superuser:
            self.fields.append('author')
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    """
    bejaye estefade az def form_valid dar class az in mixin mishe estefade kard.
    """

    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.is_active == 'i':
                self.obj.is_active = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.is_active in ['d', 'b'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('موردی برای نمایش وجود ندارد')


class AuthorsAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_author or request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('profile')
        else:
            return redirect('profile')


class SuperUserMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('موردی برای نمایش وجود ندارد')
