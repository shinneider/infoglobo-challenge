from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from app.accounts import models


class Account(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, 
                                     write_only=True, required=False)

    def validate_password(self, value):
        if value:
            return make_password(value)
        return value

    class Meta:
        model = models.Account
        exclude = ("is_staff", "is_superuser")


class AccountCreate(Account):

    class Meta:
        model = models.Account
        exclude = ("is_staff", "is_superuser", "username")
