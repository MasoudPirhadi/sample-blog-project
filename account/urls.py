from django.contrib.auth import views
from .views import Login, Register, activate
from django.urls import path

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", Register.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done", ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

from . import views

urlpatterns += [
    path('article/', views.ArticlesView.as_view(), name='account_page'),
    path('article/create/', views.ArticleCreate.as_view(), name='article_create'),
    path('article/update/<int:pk>/', views.ArticleUpdate.as_view(), name='article_update'),
    path('article/delete/<int:pk>/', views.ArticleDelete.as_view(), name='article_delete'),
    path('', views.Profile.as_view(), name='profile'),
]
