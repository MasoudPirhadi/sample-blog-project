from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='profile/', verbose_name='تصویر پروفایل', null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_author = models.BooleanField(default=False, verbose_name='وضعیت نویسندگی')
    special_user = models.DateTimeField(default=timezone.now, verbose_name='کاربر ویژه تا')

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    def get_full_name_or_username(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.username

    is_special_user.short_description = 'وضعیت کاربر ویژه'
    is_special_user.boolean = True  # vase inke moghe namayesh dar admin panel besoorate icon true ya false beshe.
