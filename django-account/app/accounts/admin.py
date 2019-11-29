from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.accounts import models


@admin.register(models.Account)
class Account(UserAdmin):
    list_display = ['email', 'username', ]
