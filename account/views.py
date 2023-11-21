from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, PasswordResetDoneView
from account.forms import ProfileForm, SignUpForm
from account.models import User
from account.tokens import activation_token
from article_module.models import Article
from account.mixins import FormValidMixin, FieldsMixin, AuthorAccessMixin, SuperUserMixin, AuthorsAccessMixin


# Create your views here.


class ArticlesView(AuthorsAccessMixin, ListView):  # dar class ha baraye login required az mixin oun estefade mikonim.
    template_name = 'registration/home.html'
    context_object_name = 'articles'
    model = Article

    def get_queryset(self):
        query = super().get_queryset()
        if self.request.user.is_superuser:
            query = query.all().order_by('-create_date')
        else:
            query = query.filter(author=self.request.user)
        return query


class ArticleCreate(AuthorsAccessMixin, FormValidMixin, FieldsMixin, CreateView):
    model = Article
    context_object_name = 'articles'
    success_url = reverse_lazy('account_page')
    template_name = 'registration/article_create.html'
    # dalile inke inja fields ro nazashtim chon mixin sakhtim azon estefade kardim.


class ArticleUpdate(AuthorAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
    model = Article
    context_object_name = 'articles'
    success_url = reverse_lazy('account_page')
    template_name = 'registration/article_create.html'


class ArticleDelete(SuperUserMixin, DeleteView):
    model = Article
    context_object_name = 'articles'
    success_url = reverse_lazy('account_page')
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    context_object_name = 'profiles'
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        """
            baraye etelaate profile ke niaz be id nabashe va vakeshi anjam beshe mitonim az get object estefade konim
            ke beshe etelaat ro vakeshi kard va niaz be ezafe kardane id dar url nabashe.
        """
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        """
        az in tarigh user haro mifrestim be form ha baraye inke not editable ha baraye superuser ha faal nabashe va
        dastresi baraye taghirat besoorate kamel dashte bashan.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy('account_page')
        else:
            return reverse_lazy('profile')


class Register(CreateView):
    template_name = 'registration/register_form.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        validlink = 'email'
        mail_subject = 'فعالسازی حساب کاربری'
        message = render_to_string(template_name='registration/acivate_account.html', context={
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': activation_token.make_token(user)

        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[to_email])
        email.send()
        return render(self.request, 'registration/register_confirm.html', {'validlink': validlink})


# activate account progress
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        validlink = False
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        validlink = False
        user = None

    if user is not None and activation_token.check_token(user, token):
        validlink = True
        user.is_active = True
        user.save()
        return render(request, 'registration/register_confirm.html', {'validlink': validlink})
    else:
        return render(request, 'registration/register_confirm.html', {'validlink': validlink})
