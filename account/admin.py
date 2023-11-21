from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# az fieldsets estefade mishe ta field hayi ke khodemon add kardim dide beshan dar admin panel va brocket hayi ke jolosh
# gozashtam vase ine ke az auth.admin.py khode django bakhshe dasteresi ha be insoorat varedesh mishodim.
UserAdmin.fieldsets[2][1]['fields'] = ("is_active",
                                       "is_staff",
                                       "is_superuser",
                                       'is_author',
                                       'special_user',
                                       "groups",
                                       "user_permissions",)

UserAdmin.list_display += ('is_author', 'is_special_user')

admin.site.register(User, UserAdmin)
